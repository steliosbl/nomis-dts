import os.path
import sys
from configparser import ConfigParser
import json

"""
I used the print statements for debugging, obviously, but i left them in since they may be helpful for logging
"""


DEFAULT_PATH = './config.json'
MAX_SIZE = 1000000  # arbitrary for now, idk


class ArgsPlaceholder:
    def __init__(self):
        self.config_path = "./test.jsonn"


args = ArgsPlaceholder()


class ConfigManager:
    def __init__(self):

        self.config = None
        self.default = None

        if not os.path.exists(DEFAULT_PATH):    # Ensures that the default path does contain the default config file. If not, then construct it
            print('No file found at the default path, new default file created.')
            self.write_default()

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

        test_string = json.dumps(self.config, indent=2)  # debugging shit
        print(test_string)

    def write_default(self):
        # subject to change, obviously
        temp = '''
        {
          "Credentials": [
            {
              "username": null,
              "password": null,
              "key": null
            }
          ],
          "Connection Information": [
            {
              "address": "127.0.0.1",
              "port": "8491"
            }
          ],
          "Dataset Information": [
            {
              "input format": null,
              "output format": "JSON",
              "data type": "Data",
              "size": null
            }
          ]
        }
        '''

        self.default = json.loads(temp)
        with open(DEFAULT_PATH, 'w') as f:
            json.dump(self.default, f, indent=2)

    def decode_into_configuration(self):

        try:
            input_format = self.config['Dataset Information'][0]['input format']
        except:
            input_format = None

        try:
            output_format = self.config['Dataset Information'][0]['output format']
        except:
            output_format = None

        try:
            data_type = self.config['Dataset Information'][0]['data type']
        except:
            data_type = None

        try:
            dataset_size = self.config['Dataset Information'][0]['dataset size']
        except:
            dataset_size = None

        return Configuration(input_format, output_format, data_type, dataset_size)

    def decode_into_connection_info(self):

        try:
            address = self.config['Connection Information'][0]['address']
        except:
            address = None

        try:
            port = self.config['Connection Information'][0]['port']
        except:
            port = None

        try:
            username = self.config['Credentials'][0]['username']
        except:
            username = None

        try:
            password = self.config['Credentials'][0]['password']
        except:
            password = None

        try:
            key = self.config['Credentials'][0]['key']
        except:
            key = None

        return ApiConnectionInfo(address, port, username, password, key)


class Configuration:
    def __init__(self, input_format, output_format, data_type, dataset_size):
        self.input_format = input_format
        self.output_format = output_format
        self.data_type = data_type  # i.e. data or metadata
        self.dataset_size = dataset_size  # i.e. the number of rows in an unweighted dataset
        self.acceptable_formats = ["json", "csv"]    # will be a list of acceptable input/output data formats for validation purposes
        self.is_valid = None

    def validate(self):
        """
        Mandatory: input_format, output_format
        Optional: data_type, size
        """
        if self.is_valid is not None:
            return self.is_valid

        self.is_valid = True

        try:
            if self.input_format is None \
                    or self.input_format.lower() not in self.acceptable_formats:
                raise Exception
            else:
                print(f"Input format {self.input_format} is valid.")
        except:
            print(f"Input format {self.input_format} is invalid.")
            self.is_valid = False

        try:
            if self.output_format is None \
                    or self.output_format.lower() not in self.acceptable_formats:
                raise Exception
            else:
                print(f"Output format {self.output_format} is valid.")
        except:
            print(f"Output format {self.output_format} is invalid.")
            self.is_valid = False

        if self.data_type is not None:
            try:
                if self.data_type.lower() != "data" \
                        or self.data_type.lower() != "metadata":
                    raise Exception
                else:
                    print(f"Data type {self.data_type} is valid.")
            except:
                print(f"Data type {self.data_type} is invalid.")
                self.is_valid = False
        else:
            print("No data type inputted, but since not mandatory. will pass.")

        if self.dataset_size is not None:
            try:
                if self.dataset_size > MAX_SIZE:
                    print(f"Size {self.dataset_size} is invalid, above maximum.")
                    self.is_valid = False
                else:
                    print(f"Size {self.dataset_size} is valid.")
            except:
                print("Size invalid, but since not mandatory, will pass.")
        else:
            print("No size inputted, but since not mandatory, will pass.")

        # No False returned, so must be valid
        return self.is_valid


class ApiConnectionInfo:
    def __init__(self, address, port, username, password, key):
        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.key = key
        self.is_valid = None

    def validate(self):
        """
        All attributes are mandatory; has defaults for address and port
        """
        if self.is_valid is not None:
            return self.is_valid

        self.is_valid = True

        try:
            split = self.address.split(".")
            if len(split) != 4:
                raise Exception
            else:
                for num in split:
                    if not (0 <= int(num) <= 255):
                        raise Exception
            print(f"The address {self.address} is valid")
        except:
            print(f"The address {self.address} not valid. Using default, 127.0.0.1, instead.")
            self.address = "127.0.0.1"

        try:
            if 0 <= int(self.port) <= 49151:
                print(f"The port {self.port} is valid.")
            else:
                raise Exception
        except:
            print(f"The port {self.port} is not valid, using default, 8491, instead.")
            self.port = "8491"

        if self.username is None:
            print("Username invalid, none inputted.")
            self.is_valid = False

        if self.password is None:
            print("Password invalid, none inputted.")
            self.is_valid = False

        if self.key is None:
            print("Key invalid, none inputted.")
            self.is_valid = False

        return self.is_valid



c = ConfigManager()
config = c.decode_into_configuration()
api_connection_info = c.decode_into_connection_info()
print(config.validate())
print(api_connection_info.validate())


