import json
from type_hints import *
from configuration import Configuration
from connection_info import ConnectionInfo
from credentials import Credentials
from config_constants import DEFAULT_PATH, DEFAULT_CONFIG_FILE
from arguments import Arguments
from logging import getLogger
from file_reader import FileReader
logger = getLogger('DTS-Logger')


class ConfigManager:
    """Class for handling the program configuration

    :param args: An instance of the arguments manager, which may contain an alternate config file
    """
    config: Union[dict, None]
    default: Union[dict, None]

    def __init__(self, args: Arguments = None) -> None:

        self.config = None
        self.default = None

        # Ensure that the default path does contain the default config file. If not, then construct it
        with FileReader(DEFAULT_PATH) as fr:
            try:
                fr.exists()
                self.default = fr.load_json()
            except FileNotFoundError:
                logger.info(f'No file found at the default path ({DEFAULT_PATH}), new default file created.')
                fr.write_json(json.loads(DEFAULT_CONFIG_FILE))
                self.default = fr.load_json()
            except ValueError:
                # Will except here if the current file at the default path is invalid in any way
                logger.info(f'File at the default path ({DEFAULT_PATH}) is invalid, new default file created.')
                fr.write_json(json.loads(DEFAULT_CONFIG_FILE))
                self.default = fr.load_json()

        if args is not None and args.config_file is not None:
            with FileReader(args.config_file) as fr:
                try:
                    if not fr.file.lower().endswith(".json") or not fr.exists():
                        raise ValueError
                    self.config = fr.load_json()
                    logger.info(f"Inputted file at ({fr.file}) used as config.")
                except (ValueError, AttributeError):
                    # Excepts if the file retrieved from args is invalid at all (syntactically or just doesn't exist)
                    logger.info(f"Inputted file path ({fr.file}) either not found or is invalid.")

                    self.config = self.default
        else:
            self.config = self.default

    def __enter__(self) -> 'ConfigManager':
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    def write_default(self) -> None:
        """Write a default config file if one doesn't exist
        """
        self.default = json.loads(DEFAULT_CONFIG_FILE)
        with open(DEFAULT_PATH, 'w') as f:
            json.dump(self.default, f, indent=2)

    def decode_credentials(self, key: str) -> Credentials:
        """Create an instance of Credentials based on the content in the config file for the 'key' parameter

        :return: A valid instance of Credentials
        """
        try:
            creds = json.dumps(self.config[key])
        except KeyError:
            logger.info(f"Config file does not contain sufficient {key}. Using default")
            creds = json.dumps(self.default[key])
        return json.loads(creds, object_hook=lambda d: Credentials(**d))

    def decode_connection_info(self, key: str) -> ConnectionInfo:
        """Create an instance of ConnectionInfo based on the content the config file for the 'key' parameter

        :return: A valid instance of ConnectionInfo
        """
        try:
            conn_info = json.dumps(self.config[key])
        except KeyError:
            logger.info(f"Config file does not contain sufficient {key}. Using default config.")
            conn_info = json.dumps(self.default[key])
        return json.loads(conn_info, object_hook=lambda d: ConnectionInfo(**d))

    def decode_configuration(self) -> Configuration:
        """Create an instance of Configuration by combining an instances of Credentials and ConnectionInfo for each of
        the APIs that the program will communicate with.

        :return: An instance of Configuration
        """
        cantabular_connection_info = self.decode_connection_info("Cantabular Connection Information")
        cantabular_credentials = self.decode_credentials("Cantabular Credentials")
        nomis_connection_info = self.decode_connection_info("Nomis Connection Information")
        nomis_credentials = self.decode_credentials("Nomis Credentials")
        nomis_metadata_connection_info = self.decode_connection_info("Nomis Metadata Connection Information")
        nomis_metadata_credentials = self.decode_credentials("Nomis Metadata Credentials")

        cantabular_connection_info.validate()
        cantabular_credentials.validate()
        nomis_connection_info.validate()
        nomis_credentials.validate()
        nomis_metadata_connection_info.validate()
        nomis_metadata_credentials.validate()

        return Configuration(
            cantabular_connection_info, cantabular_credentials,
            nomis_connection_info, nomis_credentials,
            nomis_metadata_connection_info, nomis_metadata_credentials
        )
