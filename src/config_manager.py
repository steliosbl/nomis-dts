from config_constants import DEFAULT_PATH, DEFAULT_CONFIG_FILE
from connection_info import ConnectionInfo
from configuration import Configuration
from credentials import Credentials
from file_reader import FileReader
from type_hints import *
from arguments import Arguments
from logging import getLogger
import json
logger = getLogger('DTS-Logger')


class ConfigManager:
    """
    Class for handling the program configuration, including reading from default or customised file paths, writing
    default files, and decoding JSON configuration into relevant classes

    :param args: An instance of the arguments manager, which may contain an alternate config file

    :ivar config: A python dict containing the contents of the config file that the program will use.
    :vartype config: dict
    :ivar default: A python dict containing the default configuration information, in case the inputted or enforced one
        contains errors.
    :vartype default: dict
    """

    # config: Union[dict, None]
    # default: Union[dict, None]

    def __init__(self, args: Arguments = None) -> None:

        self.config = {}
        self.default = {}

        # Ensure that the default path does contain the default config file. If not, then construct it
        with FileReader(DEFAULT_PATH) as fr:
            try:
                fr.exists()
                self.default = fr.load_json()
            except FileNotFoundError:
                logger.debug(f'No file found at the default path ({DEFAULT_PATH}), new default file created.')
                fr.write_json(json.loads(DEFAULT_CONFIG_FILE))
                self.default = fr.load_json()
            except ValueError:
                # Will except here if the current file at the default path is invalid in any way
                logger.debug(f'File at the default path ({DEFAULT_PATH}) is invalid, new default file created.')
                fr.write_json(json.loads(DEFAULT_CONFIG_FILE))
                self.default = fr.load_json()

        if args is not None and args.config_file is not None:
            with FileReader(args.config_file) as fr:
                try:
                    if not fr.file.lower().endswith(".json") or not fr.exists():
                        raise ValueError
                    self.config = fr.load_json()
                    logger.debug(f"Inputted file at ({fr.file}) used as config.")
                except (ValueError, AttributeError):
                    # Excepts if the file retrieved from args is invalid at all (syntactically or just doesn't exist)
                    logger.debug(f"Inputted file path ({fr.file}) either not found or is invalid.")

                    self.config = self.default
        else:
            self.config = self.default

    def __enter__(self) -> 'ConfigManager':
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    def write_default(self) -> None:
        """
        Write a default config file if one doesn't exist, utilising the `FileReader` class.
        """
        self.default = json.loads(DEFAULT_CONFIG_FILE)
        with open(DEFAULT_PATH, 'w') as f:
            json.dump(self.default, f, indent=2)

    def decode_credentials(self, key: str) -> Credentials:
        """
        Create an instance of Credentials based on the content in the config file for the 'key' parameter.

        :return: A valid instance of `Credentials`.
        """
        try:
            creds = json.dumps(self.config[key])
        except KeyError:
            logger.debug(f"Config file does not contain sufficient {key}. Using default")
            creds = json.dumps(self.default[key])
        if "username" not in creds:
            raise KeyError(f"{key} missing 'username' attribute.")
        if "password" not in creds:
            raise KeyError(f"{key} missing 'password' attribute.")
        if "key" not in creds:
            raise KeyError(f"{key} missing 'key' attribute.")
        return json.loads(creds, object_hook=lambda d: Credentials(**d))

    def decode_connection_info(self, key: str) -> ConnectionInfo:
        """
        Create an instance of ConnectionInfo based on the content the config file for the 'key' parameter.

        :param key: This corresponds to the name of the attribute in the JSON config file that contains the connection
            information for a certain API - e.g. 'Nomis Connection Information'.
        :return: A valid instance of `ConnectionInfo`.
        """
        try:
            conn_info = json.dumps(self.config[key])
        except KeyError:
            logger.info(f"Config file does not contain sufficient {key}. Using default config.")
            conn_info = json.dumps(self.default[key])
        if "address" not in conn_info:
            raise KeyError(f"{key} missing 'address' attribute.")
        if "port" not in conn_info:
            raise KeyError(f"{key} missing 'port' attribute.")
        return json.loads(conn_info, object_hook=lambda d: ConnectionInfo(**d))

    def decode_geography_variables(self, key: str) -> List[str]:
        """
        Create an instance of the geography variables based on the content of the config file for the 'key' parameter

        :param key: The 'key' corresponding to the Geography variables in the config file.
        :return: A list containing the geography variables.
        """
        try:
            geography_variables = json.dumps(self.config[key])
        except KeyError:
            logger.info(f"Config file does not contain sufficient {key}. Using default config.")
            geography_variables = json.dumps(self.default[key])

        return json.loads(geography_variables)

    def decode_configuration(self) -> Configuration:
        """
        Create an instance of Configuration by combining an instances of Credentials and ConnectionInfo for each of
        the APIs that the program will communicate with.

        :return: A validated instance of `Configuration`.
        """

        # Establish the APIs included in the config file
        api_config_details = [
            # FORMAT: ("API Name", "Credentials key", "Connection info key"),
            ("cantabular", "Cantabular Credentials", "Cantabular Connection Information"),
            ("nomis", "Nomis Credentials", "Nomis Connection Information"),
            ("nomis_metadata", "Nomis Metadata Credentials", "Nomis Metadata Connection Information")
        ]

        # Create a dictionary containing the names of the APIs as keys, and namedtuples containing instances of
        # Credentials and ConnectionInfo for each API as values; all as specified in the configurable list above
        configurations = {
            name.lower(): CredentialsConninfo(self.decode_credentials(creds), self.decode_connection_info(conn))
            for name, creds, conn in api_config_details
        }

        for api in configurations:
            configurations[api].credentials.validate()
            configurations[api].connection_info.validate()

        # Add the geography to the configurations
        variables = {"geography": self.decode_geography_variables("Geography Variables")}

        return Configuration(configurations, variables)
