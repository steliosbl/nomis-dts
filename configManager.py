import os.path
import sys
import json
from configuration import Configuration
from apiConnectionInfo import ConnectionInfo, Credentials, ApiConnectionInfo
from configConstants import DEFAULT_PATH, DEFAULT_CONFIG_FILE

"""
I used the print statements for debugging, obviously, but i left them in since they may be helpful for logging
"""


class ArgsPlaceholder:
    def __init__(self):
        self.config_path = "./test.json"


args = ArgsPlaceholder()


class ConfigManager:
    def __init__(self):

        self.config = None
        self.default = None

        if not os.path.exists(DEFAULT_PATH):    # Ensures that the default path does contain the default config file. If not, then construct it
            print('No file found at the default path, new default file created.')
            self.write_default()
        else:
            with open(DEFAULT_PATH) as f:
                self.default = json.loads(f.read())

        try:
            path = args.config_path
            if not path.lower().endswith('.json') \
                    or not os.path.exists(path):  # Ensures this file exists and is indeed a json file
                raise ValueError
            with open(path) as f:
                self.config = json.loads(f.read())
                print("Inputted file used as config.")
        except (ValueError, AttributeError):    # Will except if the file retrieved from args is invalid at all (syntactically or just doesn't exist)
            print("Inputted (file at) path either not found or is invalid.")
            try:
                with open(DEFAULT_PATH) as f:
                    self.config = json.loads(f.read())
                    print("Default config file used.")
            except ValueError:  # Will except here if the current file at the default path is invalid in any way
                print("Problem with file at default path, rebuilding...")
                self.write_default()    # All else fails, a new default file is built
                self.config = self.default
        except Exception as e:
            print(f"An unforeseen error occurred managing the config file(s). ({e})")
            sys.exit()

        # Debugging:
        # test_string = json.dumps(self.config, indent=2)
        # print(test_string)

    def write_default(self) -> None:
        self.default = json.loads(DEFAULT_CONFIG_FILE)
        with open(DEFAULT_PATH, 'w') as f:
            json.dump(self.default, f, indent=2)

    def decode_into_configuration(self) -> Configuration:
        try:
            config_info = json.dumps(self.config["Dataset Information"])
        except:
            print("Config file does not contain sufficient dataset information. Using default.")
            config_info = json.dumps(self.default["Dataset Information"])
        return json.loads(config_info, object_hook=lambda d: Configuration(**d))

    def decode_into_cantabular_credentials(self) -> Credentials:
        try:
            creds = json.dumps(self.config["Cantabular Credentials"])
        except:
            print("Config file does not contain sufficient Cantabular credentials. Using default")
            creds = json.dumps(self.default["Cantabular Credentials"])
        return json.loads(creds, object_hook=lambda d: Credentials(**d))

    def decode_into_cantabular_connection_info(self) -> ConnectionInfo:
        try:
            conn_info = json.dumps(self.config["Cantabular Connection Information"])
        except:
            print("Config file does not contain sufficient Cantabular connection information. Using default config.")
            conn_info = json.dumps(self.default["Cantabular Connection Information"])
        return json.loads(conn_info, object_hook=lambda d: ConnectionInfo(**d))

    def decode_into_nomis_credentials(self) -> Credentials:
        try:
            creds = json.dumps(self.config["Nomis Credentials"])
        except:
            print("Config file does not contain sufficient Nomis credentials.")
            creds = json.dumps(self.default["Nomis Credentials"])
        return json.loads(creds, object_hook=lambda d: Credentials(**d))

    def decode_into_nomis_connection_info(self) -> ConnectionInfo:
        try:
            conn_info = json.dumps(self.config["Nomis Connection Information"])  # gets the connection information from the config
        except:
            print("Config file does not contain sufficient Nomis connection information.")
            conn_info = json.dumps(self.default["Nomis Connection Information"])
        return json.loads(conn_info, object_hook=lambda d: ConnectionInfo(**d)) # reloads this info into the connection info object


def create_api_connection_info(credentials: Credentials, connection_info: ConnectionInfo) -> ApiConnectionInfo:
    return ApiConnectionInfo(credentials.username, credentials.password, credentials.key,
                             connection_info.api, connection_info.address, connection_info.port)



