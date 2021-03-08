import os.path
import sys
import json
from configuration import Configuration
from api_connection_info import ConnectionInfo, Credentials, ApiConnectionInfo
from config_constants import DEFAULT_PATH, DEFAULT_CONFIG_FILE
from args_manager import ArgsManager


class ConfigManager:
    """Class for handling the program configuration

    :param args: An instance of the arguments manager, which may contain an alternate config file
    :type args: :class:ArgsManager, optional
    """
    def __init__(self, args: ArgsManager = None) -> None:

        self.config = None
        self.default = None

        # Ensure that the default path does contain the default config file. If not, then construct it
        if not os.path.exists(DEFAULT_PATH):
            print('No file found at the default path, new default file created.')
            self.write_default()
        else:
            with open(DEFAULT_PATH) as f:
                self.default = json.loads(f.read())

        if args is not None and args.config:
            try:
                path = args.config_path
                # Ensure this file exists and is indeed a json file
                if not path.lower().endswith('.json') \
                        or not os.path.exists(path):
                    raise ValueError
                with open(path) as f:
                    self.config = json.loads(f.read())
                    print("Inputted file used as config.")
            except (ValueError, AttributeError):
                # Will except if the file retrieved from args is invalid at all (syntactically or just doesn't exist)
                print("Inputted (file at) path either not found or is invalid.")
                try:
                    with open(DEFAULT_PATH) as f:
                        self.config = json.loads(f.read())
                        print("Default config file used.")
                except ValueError:
                    # Will except here if the current file at the default path is invalid in any way
                    # Since all else failed, a new default file is built
                    print("Problem with file at default path, rebuilding...")
                    self.write_default()
                    self.config = self.default
            except Exception as e:
                print(f"An unforeseen error occurred managing the config file(s). ({e})")
                sys.exit()

    def write_default(self) -> None:
        """Write a default config file if one doesn't exist
        """
        self.default = json.loads(DEFAULT_CONFIG_FILE)
        with open(DEFAULT_PATH, 'w') as f:
            json.dump(self.default, f, indent=2)

    def decode_into_configuration(self) -> Configuration:
        """Create an instance of Configuration based on the content of the config file

        :return: A valid instance of Configuration
        :rtype: :class:Configuration
        """
        try:
            config_info = json.dumps(self.config["Dataset Information"])
        except:
            print("Config file does not contain sufficient dataset information. Using default.")
            config_info = json.dumps(self.default["Dataset Information"])
        return json.loads(config_info, object_hook=lambda d: Configuration(**d))

    def decode_into_cantabular_credentials(self) -> Credentials:
        """Create an instance of Credentials based on the Cantabular content in the config file

        :return: A valid instance of Credentials for Cantabular
        :rtype: :class:Credentials
        """
        try:
            creds = json.dumps(self.config["Cantabular Credentials"])
        except:
            print("Config file does not contain sufficient Cantabular credentials. Using default")
            creds = json.dumps(self.default["Cantabular Credentials"])
        return json.loads(creds, object_hook=lambda d: Credentials(**d))

    def decode_into_cantabular_connection_info(self) -> ConnectionInfo:
        """Create an instance of ConnectionInfo based on the Cantabular content the config file

        :return: A valid instance of ConnectionInfo for Cantabular
        :rtype: :class:ConnectionInfo
        """
        try:
            conn_info = json.dumps(self.config["Cantabular Connection Information"])
        except:
            print("Config file does not contain sufficient Cantabular connection information. Using default config.")
            conn_info = json.dumps(self.default["Cantabular Connection Information"])
        return json.loads(conn_info, object_hook=lambda d: ConnectionInfo(**d))

    def decode_into_nomis_credentials(self) -> Credentials:
        """Create an instance of Credentials based on the Nomis content in the config file

        :return: A valid instance of ConnectionInfo for Nomis
        :rtype: :class:ConnectionInfo
        """
        try:
            creds = json.dumps(self.config["Nomis Credentials"])
        except:
            print("Config file does not contain sufficient Nomis credentials.")
            creds = json.dumps(self.default["Nomis Credentials"])
        return json.loads(creds, object_hook=lambda d: Credentials(**d))

    def decode_into_nomis_connection_info(self) -> ConnectionInfo:
        """Create an instance of ConnectionInfo based on the Nomis content the config file

        :return: A valid instance of ConnectionInfo for Nomis
        :rtype: :class:ConnectionInfo
        """
        # Get the connection information from the config
        try:
            conn_info = json.dumps(self.config["Nomis Connection Information"])
        except:
            print("Config file does not contain sufficient Nomis connection information.")
            conn_info = json.dumps(self.default["Nomis Connection Information"])
        # Reload this info into the connection info object
        return json.loads(conn_info, object_hook=lambda d: ConnectionInfo(**d))

    def create_api_connection_info(self, credentials: Credentials,
                                   connection_info: ConnectionInfo) -> ApiConnectionInfo:
        """Create an instance of ApiConnectionInfo by combining an instance of Credentials with an instance of ConnectionInfo

        :param credentials: A valid Credentials class for either Nomis or Cantabular
        :type credentials: :class:Credentials
        :param connection_info: A valid ConnectionInfo class for either Nomis or Cantabular
        :type connection_info: :class:ConnectionInfo

        :return: An instance of ApiConnectionInfo for either Nomis or Cantabular
        :rtype: :class:ApiConnectionInfo
        """
        return ApiConnectionInfo(credentials.username, credentials.password, credentials.key,
                                 connection_info.api, connection_info.address, connection_info.port)
