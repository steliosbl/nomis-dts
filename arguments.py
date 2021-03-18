from file_reader import FileReader
from type_hints import *
import argparse
import os


class Arguments:
    """Container class for the program's arguments; includes method for validating the arguments.

    :param arguments: Parsed argparse object containing the arguments for the program

    :ivar metadata: Read in as a string and resolved to a Boolean: indicates whether the metadata or normal (i.e. data)
    program pipeline is used
    :ivar filename: Location of a file to read from instead of querying Cantabular
    :ivar query_variables: Parameter for querying Cantabular
    :ivar dataset_id: Parameter for querying Cantabular
    :ivar dataset_title: Parameter for querying Cantabular
    :ivar query_dataset: Parameter for querying Cantabular
    :ivar suppress_prompts: Toggle for suppressing prompts
    :ivar verbose: Toggle for a verbose out during runtime
    :ivar log_file: For overriding the default location of the log file
    :ivar config_file: For overriding the default location of the config file
    """

    # Metadata toggle
    metadata: Union[str, bool]

    # Location of a file to read from instead of querying Cantabular
    filename: Union[str, None]

    # Parameters for querying Cantabular
    query_variables: Union[List[str], str, None]
    dataset_id: Union[str, None]
    dataset_title: Union[str, None]
    query_dataset: Union[str, None]

    # Flags for toggling prompts to be suppressed of a verbose run
    suppress_prompts: bool
    verbose: bool

    # For overriding the default location of the log/config files
    log_file: Union[str, None]
    config_file: Union[str, None]

    def __init__(self, arguments: argparse.Namespace) -> None:
        self.metadata = arguments.metadata
        self.metadata_format = arguments.metadata_format
        self.filename = arguments.filename
        self.query_variables = arguments.query_variables
        self.dataset_id = arguments.dataset_id
        self.dataset_title = arguments.dataset_title
        self.query_dataset = arguments.query_dataset
        self.suppress_prompts = arguments.suppress_prompts
        self.verbose = arguments.verbose
        self.log_file = arguments.log_file
        self.config_file = arguments.config_file

    def validate(self) -> bool:
        """Method for validating the arguments, and raising an exception in the case of anything invalid.

        :return: Returns True upon successful validation; otherwise, an exception will have been raised
        :raises ValueError: If any included argument contains an empty string, or any required argument is excluded
        :raises FileNotFoundError: If the inputs for filename or config_file aren't paths to existing files
        :raises IOError: If the arguments for filename or config_file aren't .json, or log_file isn't .log
        """
        # Resolve metadata
        if self.metadata == 'metadata':
            self.metadata = True
        elif self.metadata == 'data':
            self.metadata = False
        else:
            raise ValueError("Program only supports 'data' or 'metadata' modes.")

        if self.metadata:
            if self.metadata_format is None:
                raise ValueError("Must include metadata format (-r flag) to handle metadata.")
            elif self.metadata_format != 'O' and self.metadata_format != 'C':
                raise ValueError("Invalid argument for metadata format.")
        else:
            if self.metadata_format is not None:
                print("-r flag will be ignored.")
            if self.dataset_id is None:
                raise ValueError("Must include dataset id (-i flag) if not handling metadata.")
            if self.dataset_title is None:
                raise ValueError("Must include dataset title (-t flag) if not handling metadata.")

        if self.filename is None:
            if self.metadata:
                raise ValueError("Currently this utility only supports reading from a file for metadata.")
            else:
                if self.query_variables is None:
                    raise ValueError("Must include query variables (-q flag) if not using a file.")
                if self.query_dataset is None:
                    raise ValueError("Must include query dataset (-d flag) if not using a file.")

                self.query_variables = self.query_variables.split(", ")
                for s in self.query_variables:
                    if len(s) == 0:
                        raise ValueError("query_variable contains empty strings")

        elif not self.metadata:
            ignore: List[str] = []
            if self.query_variables is not None:
                ignore.append("-q")
            if self.query_dataset is not None:
                ignore.append("-d")
            if len(ignore) > 0:
                if not self.suppress_prompts:
                    print(f"--- THE -f FLAG WAS USED, YET THE FOLLOWING FLAGS WERE ALSO USED: {', '.join(ignore)}. ---"
                          f"\n*** PROCEED TO READ FROM FILE y/n ***")
                    while True:
                        r = input()
                        if r.lower() == 'n':
                            if len(ignore) != 4:
                                raise ValueError("Insufficient arguments for querying Cantabular; program halting.")
                            else:
                                self.filename = None
                                break
                        elif r.lower() == 'y':
                            break
                        else:
                            print("Invalid response, please input y (YES) or n (NO).")
            if self.filename is not None:
                if not self.filename.lower().endswith(".json"):
                    raise IOError(f"Inputted query file ({self.filename}) must be a valid json!")
                with FileReader(self.filename) as fr:
                    fr.exists()

        if self.log_file is not None and not self.log_file.endswith(".log"):
            raise FileNotFoundError(f"Inputted log file ({self.log_file}) not a valid .log file. Program halting.")

        if self.config_file is not None:
            if not self.config_file.lower().endswith(".json"):
                raise IOError(f"Inputted config file ({self.config_file}) must be a valid json!")
            with FileReader(self.config_file) as fr:
                fr.exists()

        return True
