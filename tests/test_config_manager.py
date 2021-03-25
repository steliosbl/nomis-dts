import sys; sys.path.append('..')
import unittest
from config_manager import ConfigManager
from configuration import Configuration
from connection_info import ConnectionInfo
from credentials import Credentials
import config_constants
from collections import namedtuple

"""
Prerequisites:
 - None

Test all: 
 - python test_config_manager.py 

"""


VALID_CONFIG_FILE = '''
{
  "Cantabular Credentials": {
    "username": "durham.project",
    "password": "extra.carrot.slowly",
    "key": null
  },
  "Cantabular Connection Information": {
    "address": "https://ftb-api-ext.ons.sensiblecode.io",
    "port": null
  },
  "Nomis Credentials": {
    "username": "user",
    "password": "pass",
    "key": null
  },
  "Nomis Connection Information": {
    "address": "https://localhost",
    "port": "5001"
  },
  "Nomis Metadata Credentials": {
    "username": "user",
    "password": "pass",
    "key": null
  },
  "Nomis Metadata Connection Information": {
    "address": "https://localhost",
    "port": "5005"
  }
}
'''

INVALID_CONFIG_FILE = '''
{
  "Cantabular Credentials": {
    "username": "durham.project",
    "password": "extra.carrot.slowly",
    "key": null
  },
  "Cantabular Connection Information": {
    "address": "https://ftb-api-ext.ons.sensiblecode.io",
    "port": null
  },
  "Nomis Credentials": {
    "username": "user",
    "password": "pass",
    "key": null
  },
  "Nomis Connection Information": {
    "address": "https://localhost",
    "port": "5001"
  }
}
'''

mock_args_manager = namedtuple("mock_args_manager", "config_file")
mock_args = mock_args_manager("test_config.json")


class TestConfigManager(unittest.TestCase):
    def setUp(self) -> None:
        """Create a valid ArgsManager instance for use in the following tests
        """
        self.config_manager = ConfigManager(mock_args)

    def test_constants(self) -> None:
        """Ensure the test constants are of the correct type
        """
        self.assertIsInstance(config_constants.DEFAULT_PATH, str)
        self.assertIsInstance(config_constants.DEFAULT_CONFIG_FILE, str)

    def test_default_config_file(self):
        """Test the default_config_file, i.e. ensure that the ArgsManager's default config file attribute is valid
        """
        self.assertIsInstance(self.config_manager.default, dict)
        self.assertIn("Cantabular Credentials", self.config_manager.default)
        self.assertIn("Cantabular Connection Information", self.config_manager.default)
        self.assertIn("Nomis Credentials", self.config_manager.default)
        self.assertIn("Nomis Connection Information", self.config_manager.default)
        self.assertIn("Nomis Metadata Credentials", self.config_manager.default)
        self.assertIn("Nomis Metadata Connection Information", self.config_manager.default)

    def test_config_file(self):
        """Test the ArgsManager's ability to read in a config file from a custom location, and handle appropriately
        """
        self.assertIsInstance(self.config_manager.config, dict)
        self.assertIn("Cantabular Credentials", self.config_manager.default)
        self.assertIn("Cantabular Connection Information", self.config_manager.default)
        self.assertIn("Nomis Credentials", self.config_manager.default)
        self.assertIn("Nomis Connection Information", self.config_manager.default)
        self.assertIn("Nomis Metadata Credentials", self.config_manager.default)
        self.assertIn("Nomis Metadata Connection Information", self.config_manager.default)

    def test_decode_credentials(self):
        """Test the decode_credentials() method using invalid parameters and asserting that the expected outcome occurs
        upon valid calls
        """

        with self.assertRaises(KeyError):
            self.config_manager.decode_credentials("Nomis Connection Info")

        # Verify that the decode_credentials() method returns a valid instance of Credentials, and that the
        # .validate() method of such works (integration testing)
        cantabular_creds = self.config_manager.decode_credentials("Cantabular Credentials")
        nomis_creds = self.config_manager.decode_credentials("Nomis Credentials")
        nomis_metadata_creds = self.config_manager.decode_credentials("Nomis Metadata Credentials")
        for creds in (cantabular_creds, nomis_creds, nomis_metadata_creds):
            self.assertIsInstance(creds, Credentials)
            self.assertTrue(creds.validate())

    def test_decode_connection_info(self):
        """Test the decode_connection_info() class: ensure invalid attempts elicit the expected exception, and ensure
        that integration works such that the methods of ConnectionInfo are functional
        """

        with self.assertRaises(KeyError):
            self.config_manager.decode_connection_info("Cantabular Credentials")

        # Verify that the decode_connection_info() method returns a valid instance of ConnectionInfo, and that the
        # .validate() method of such works (integration testing)
        cantabular_info = self.config_manager.decode_connection_info("Cantabular Connection Information")
        nomis_info = self.config_manager.decode_connection_info("Nomis Connection Information")
        nomis_metadata_info = self.config_manager.decode_connection_info("Nomis Metadata Connection Information")
        for info in (cantabular_info, nomis_info, nomis_metadata_info):
            self.assertIsInstance(info, ConnectionInfo)
            self.assertTrue(info.validate())

    def test_decode_configuration(self):
        """Test the decode_configuration() method works as expected, and assert that the returned instance of
        Configuration also works as expected
        """
        config = self.config_manager.decode_configuration()
        self.assertIsInstance(config, Configuration)
        print(config.get_client("cantabular"))

    def test_invalid_connection_info(self):
        inv_con_info_1 = ConnectionInfo("unresolvable-address.not.real", 5001)
        with self.assertRaises(ValueError):
            inv_con_info_1.validate()
        inv_con_info_2 = ConnectionInfo("http://localhost", 100000)
        with self.assertRaises(ValueError):
            inv_con_info_2.validate()

    def test_invalid_credentials(self):
        inv_creds_1 = Credentials("string", 99, None)
        with self.assertRaises(TypeError):
            inv_creds_1.validate()
        inv_creds_2 = Credentials("", "string", "key")
        with self.assertRaises(ValueError):
            inv_creds_2.validate()


if __name__ == '__main__':
    unittest.main()
