import unittest
from config_manager import ConfigManager
from configuration import Configuration
from api_connection_info import ConnectionInfo, Credentials, ApiConnectionInfo
import config_constants
from collections import namedtuple

VALID_CONFIG_FILE = '''
{
  "Cantabular Credentials": {
    "username": null,
    "password": null,
    "key": null
  },
  "Cantabular Connection Information": {
    "api": "cantabular",
    "address": "localhost",
    "port": "8491"
  },
  "Nomis Credentials": {
    "username": null,
    "password": null,
    "key": null
  },
  "Nomis Connection Information": {
    "api": "nomis",
    "address": "https://www.nomisweb.co.uk/api/v2",
    "port": "1234"
  },
  "Dataset Information": {
    "input_format": null,
    "output_format": "JSON",
    "data_type": "Data",
    "dataset_size": null
  }
}
'''

INVALID_CONFIG_FILE = '''
{
  "Dataset Information": {
    "input_format": null,
    "output_format": "JSON",
    "data_type": "Data",
    "dataset_size": null
  }
}
'''

mock_args_manager = namedtuple("mock_args_manager", "config, config_path")
mock_args = mock_args_manager(True, "test_config.json")


class TestConfigConstants(unittest.TestCase):
    def test_constants(self) -> None:
        self.assertIsInstance(config_constants.DEFAULT_PATH, str)
        self.assertIsInstance(config_constants.DEFAULT_CONFIG_FILE, str)
        self.assertIsInstance(config_constants.VALID_FORMATS, list)
        self.assertIn('json', config_constants.VALID_FORMATS)
        self.assertIn('csv', config_constants.VALID_FORMATS)
        self.assertIn('json-stat', config_constants.VALID_FORMATS)


class TestConfigManager(unittest.TestCase):
    def setUp(self) -> None:
        self.config_manager = ConfigManager(mock_args)

    def test_default_config_file(self):
        self.assertIsInstance(self.config_manager.default, dict)
        self.assertIn("Cantabular Credentials", self.config_manager.default)
        self.assertIn("Cantabular Connection Information", self.config_manager.default)
        self.assertIn("Nomis Credentials", self.config_manager.default)
        self.assertIn("Nomis Connection Information", self.config_manager.default)
        self.assertIn("Dataset Information", self.config_manager.default)

    def test_config_file(self):
        self.assertIsInstance(self.config_manager.config, dict)
        self.assertIn("Cantabular Credentials", self.config_manager.config)
        self.assertIn("Cantabular Connection Information", self.config_manager.config)
        self.assertIn("Nomis Credentials", self.config_manager.config)
        self.assertIn("Nomis Connection Information", self.config_manager.config)
        self.assertIn("Dataset Information", self.config_manager.config)

    def test_decode_into_configuration(self):
        result = self.config_manager.decode_into_configuration()
        self.assertIsInstance(result, Configuration)

    def test_decode_into_cantabular_credentials(self):
        result = self.config_manager.decode_into_cantabular_credentials()
        self.assertIsInstance(result, Credentials)

    def test_decode_into_cantabular_connection_info(self):
        result = self.config_manager.decode_into_cantabular_connection_info()
        self.assertIsInstance(result, ConnectionInfo)

    def test_decode_into_nomis_credentials(self):
        result = self.config_manager.decode_into_nomis_credentials()
        self.assertIsInstance(result, Credentials)

    def test_decode_into_nomis_connection_info(self):
        result = self.config_manager.decode_into_cantabular_connection_info()
        self.assertIsInstance(result, ConnectionInfo)

    def test_create_api_connection_info(self):
        nomis_credentials = self.config_manager.decode_into_nomis_credentials()
        nomis_connection_info = self.config_manager.decode_into_nomis_connection_info()
        nomis_results = self.config_manager.create_api_connection_info(nomis_credentials, nomis_connection_info)
        self.assertIsInstance(nomis_results, ApiConnectionInfo)
        cantabular_credentials = self.config_manager.decode_into_cantabular_credentials()
        cantabular_connection_info = self.config_manager.decode_into_cantabular_connection_info()
        cantabular_results = self.config_manager.create_api_connection_info(cantabular_credentials, cantabular_connection_info)
        self.assertIsInstance(cantabular_results, ApiConnectionInfo)


if __name__ == '__main__':
    unittest.main()
