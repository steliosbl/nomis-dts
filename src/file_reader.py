from type_hints import *
from logging import getLogger
import chardet
import json
import os
logger = getLogger("DTS-Logger")


class FileReader:
    """
    Class for handling files; reading, writing, and checking for existence.

    :param file: A string representing the location of a file for use in the program.
    :ivar: Initial value: file.
    :vartype file: str
    """

    file: str

    def __init__(self, file: str) -> None:
        self.file = file

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    def exists(self) -> bool:
        """
        Ensure the file exists by checking the path is an existing one.

        :raises FileNotFoundError: If the file attribute contains a string that represents a path which doesn't exist.
        :return: `True` if no exception is raised, indicating that the file is an existing one.
        """
        if not os.path.exists(self.file):
            raise FileNotFoundError(f"The file {self.file} could not be located.")
        else:
            logger.debug(f"File '{self.file}' has been found to exist.")
            return True

    def load_json(self) -> dict:
        """
        Check the encoding of the file and load it in as a json string.
        """
        enc = chardet.detect(open(self.file, 'rb').read())['encoding']
        with open(self.file, 'r', encoding=enc) as json_file:
            data = json.load(json_file)
        return data

    def write_json(self, to_write: str) -> None:
        """
        Write out a json file.
        """
        with open(self.file, 'w') as f:
            json.dump(to_write, f, indent=2)

    def write_text_file(self, to_write: str) -> None:
        """
        Write out a text file.
        """
        with open(self.file, 'w') as f:
            f.write(to_write)
