import unittest.mock
import sys
from nomis_api_connector import NomisApiConnector
import requests
import time

"""
Usage: 
 - To run all tests:        python -m unittest test_nomisApiConnector.TestValidNomisApiConnector
 
 - To run specific tests:   python -m unittest test_nomisApiConnector.TestNomisApiConnectorDatasets.[test]
        - for example, python -m unittest test_nomisApiConnector.TestNomisApiConnectorDatasets.test_dataset_exists
        -              python -m unittest test_nomisApiConnector.TestNomisApiConnectorVariables.test_variable_exists
        
 - Note: include -b flag to silence stdout


Prerequisite:
  - Nomis API must be running on port 5001
  
"""


# TEST CONSTANTS

VALID_ADDRESS:   str = 'https://localhost'
INVALID_ADDRESS: str = 'not.an.address'
PORT: str = '5001'
VALID_CREDENTIALS:   tuple = ("durham.project", " extra.carrot.slowly")  # using the cantabular creds for time being...
INVALID_CREDENTIALS: tuple = ("a", "b")

VALID_ID_1: str = "TESTID01"
VALID_ID_2: str = "TESTID02"
VALID_ID_3: str = "TESTID03"

VALID_DS_1: dict = {
  "id": VALID_ID_1,
  "title": "string",
  "contactId": "string",
  "isAdditive": True,
  "isFlagged": True,
  "derivedFrom": "string",
  "restrictedAccess": True,
  "minimumRound": 0,
  "online": True
}

VALID_DS_2: dict = {
  "id": VALID_ID_2,
  "title": "string",
  "contactId": "string",
  "isAdditive": True,
  "isFlagged": True,
  "derivedFrom": "string",
  "restrictedAccess": True,
  "minimumRound": 0,
  "online": True
}

VALID_DS_3: dict = {
  "id": VALID_ID_3,
  "title": "string",
  "contactId": "string",
  "isAdditive": True,
  "isFlagged": True,
  "derivedFrom": "string",
  "restrictedAccess": True,
  "minimumRound": 0,
  "online": True
}

INVALID_DS: dict = {
  "id": "syn01100",
  "title": "TEST 1",
  "metadata": 1,
  "contactId": None,
  "isAdditive": False,
  "isFlagged": False,
  "derivedFrom": None,
  "restrictedAccess": False,
}

VALID_DIMENSIONS = [{
  "name": "string",
  "label": "string",
  "isAdditive": True,
  "variable": {
    "name": "string",
    "view": "string"
  },
  "role": "Temporal",
  "canFilter": True,
  "defaults": [
    "string"
  ],
  "database": {
    "isKey": True,
    "index": 0,
    "defaultView": "string",
    "discontinuities": [
      {
        "view": "string",
        "causedBy": {
          "variable": "string",
          "categories": [
            "string"
          ]
        }
      }
    ]
  }
}]


VALID_OBSERVATIONS_1: dict = {
    'dataset': VALID_ID_1,
    'dimensions': ['SEX'],
    'codes': [['1', '2']],
    'values': [27517574, 28421312],
    'statuses': None
}


VALID_OBSERVATIONS_2: dict = {
    'dataset': VALID_ID_2,
    'dimensions': ['SEX'],
    'codes': [['1', '2']],
    'values': [27517574, 28421312],
    'statuses': None
}


VALID_OBSERVATIONS_ARRAY: list = [VALID_OBSERVATIONS_2, VALID_OBSERVATIONS_2, VALID_OBSERVATIONS_2]

VALID_VAR_NAME_1: str = "TEST_VARIABLE_1"
VALID_VAR_NAME_2: str = "TEST_VARIABLE_2"

VALID_VARIABLE_1: dict = {
  "name": VALID_VAR_NAME_1,
  "label": "string",
  "defaults": [
    "string"
  ]
}

VALID_VARIABLE_2: dict = {
  "name": VALID_VAR_NAME_2,
  "label": "string",
  "defaults": [
    "string"
  ]
}

VALID_CAT_CODE_1: str = "TEST_CAT_1"
VALID_CAT_CODE_2: str = "TEST_CAT_2"
VALID_CAT_CODE_3: str = "TEST_CAT_3"

VALID_CAT_1: dict = {
    "code": VALID_CAT_CODE_1,
    "title": "string",
    "keyval": 0,
    "typeId": "string",
    "ancestors": [
      {
        "code": "string",
        "hierarchies": [
          "string"
        ]
      }
    ]
  }


VALID_CAT_2: dict = {
    "code": VALID_CAT_CODE_2,
    "title": "string",
    "keyval": 0,
    "typeId": "string",
    "ancestors": [
      {
        "code": "string",
        "hierarchies": [
          "string"
        ]
      }
    ]
  }


VALID_CAT_3: dict = {
    "code": VALID_CAT_CODE_1,
    "title": "changed",
    "keyval": 0,
    "typeId": "string",
    "ancestors": [
      {
        "code": "string",
        "hierarchies": [
          "string"
        ]
      }
    ]
  }

VALID_CAT_ARR = [VALID_CAT_1, VALID_CAT_2]


# TEST CASES

class TestNomisApiConnectorDatasets(unittest.TestCase):
    def setUp(self) -> None:
        # Set up two connectors, one with a valid address and one without
        self.invalid_connector = NomisApiConnector(INVALID_CREDENTIALS, INVALID_ADDRESS)
        self.valid_connector = NomisApiConnector(VALID_CREDENTIALS, VALID_ADDRESS, PORT)

        # Create two datasets to be used in the tests
        self.valid_connector.create_dataset(VALID_ID_1, VALID_DS_1)
        self.valid_connector.create_dataset(VALID_ID_2, VALID_DS_2)

        # Assign dimensions and observations to test dataset 1
        self.valid_connector.assign_dimensions_to_dataset(VALID_ID_1, VALID_DIMENSIONS)
        self.valid_connector.append_dataset_observations(VALID_ID_1, VALID_OBSERVATIONS_1)

        self.stdout = sys.stdout

    def tearDown(self) -> None:
        # Delete the datasets created for testing purposes
        self.valid_connector.session.delete(f'{self.valid_connector.client}/Datasets/'
                                            f'{VALID_ID_1}/dimensions', verify=False)
        self.valid_connector.session.delete(f'{self.valid_connector.client}/Datasets/'
                                            f'{VALID_ID_1}/values', verify=False)
        self.valid_connector.session.delete(f'{self.valid_connector.client}/Datasets/{VALID_ID_1}', verify=False)
        self.valid_connector.session.delete(f'{self.valid_connector.client}/Datasets/{VALID_ID_2}', verify=False)

    def test_validate_ds(self) -> None:
        # Invalid
        with self.assertRaises(TypeError):
            self.invalid_connector.validate_ds("wrong")
        with self.assertRaises(TypeError):
            self.valid_connector.validate_ds("wrong")
        with self.assertRaises(KeyError):
            self.invalid_connector.validate_ds({"a": "b"})
        with self.assertRaises(KeyError):
            self.valid_connector.validate_ds({"a": "b"})

        # Valid (note, the validation should still work with a connector with a bad client)
        self.assertTrue(self.invalid_connector.validate_ds(VALID_DS_1))
        self.assertTrue(self.valid_connector.validate_ds(VALID_DS_1))

    def test_get_dataset(self) -> None:
        # Invalid/non-existing datasets
        with self.assertRaises(TypeError):
            self.invalid_connector.get_dataset(True)
        with self.assertRaises(TypeError):
            self.invalid_connector.get_dataset(1)
        with self.assertRaises(TypeError):
            self.valid_connector.get_dataset(True)
        with self.assertRaises(TypeError):
            self.valid_connector.get_dataset({"a": "b"})
        with self.assertRaises(requests.ConnectionError):
            self.assertFalse(self.invalid_connector.get_dataset(VALID_ID_1))

        # Correct methods
        valid_ds_1 = self.valid_connector.get_dataset(VALID_ID_1)
        self.assertEqual(valid_ds_1['id'], VALID_ID_1)
        valid_ds_2 = self.valid_connector.get_dataset(VALID_ID_2)
        self.assertEqual(valid_ds_2['id'], VALID_ID_2)

    def test_get_dataset_bool(self) -> None:
        # Invalid
        with self.assertRaises(requests.ConnectionError):
            self.invalid_connector.get_dataset(VALID_ID_1, return_bool=True)
        with self.assertRaises(TypeError):
            self.invalid_connector.get_dataset(1, return_bool=True)
        with self.assertRaises(TypeError):
            self.invalid_connector.get_dataset(True, return_bool=True)
        with self.assertRaises(TypeError):
            self.valid_connector.get_dataset({"a":"b"}, return_bool=True)
        with self.assertRaises(TypeError):
            self.valid_connector.get_dataset(True, return_bool=True)
        
        # Valid
        self.assertTrue(self.valid_connector.get_dataset(VALID_ID_1, return_bool = True))
        self.assertTrue(self.valid_connector.get_dataset(VALID_ID_2, return_bool = True))

    def test_create_dataset(self) -> None:
        # Invalid attempts to create dataset with various errors
        with self.assertRaises(KeyError):
            self.invalid_connector.create_dataset(VALID_ID_1, {"a": "b"})
        with self.assertRaises(KeyError):
            self.invalid_connector.create_dataset(VALID_ID_1, {"a": "b"})
        with self.assertRaises(requests.ConnectionError):
            self.invalid_connector.create_dataset(VALID_ID_1, VALID_DS_1)
        with self.assertRaises(TypeError):
            self.valid_connector.create_dataset(VALID_ID_1, "wrong")
        with self.assertRaises(KeyError):
            self.valid_connector.create_dataset(VALID_ID_1, INVALID_DS)
        with self.assertRaises(TypeError):
            self.valid_connector.create_dataset(VALID_ID_1, str(VALID_DS_1))
        with self.assertRaises(ValueError):
            self.assertFalse(self.valid_connector.create_dataset(VALID_ID_2, VALID_DS_1))

        # Valid attempt to create dataset, validly ensure its existence, then delete
        self.assertTrue(self.valid_connector.create_dataset(VALID_ID_3, VALID_DS_3))
        self.assertTrue(self.valid_connector.get_dataset(VALID_ID_3, return_bool = True))
        valid_ds = self.valid_connector.get_dataset(VALID_ID_3)
        self.assertEqual(valid_ds['id'], VALID_ID_3)
        # self.valid_connector.session.delete(f'{self.valid_connector.client}/Datasets/{VALID_ID_3}', verify=False)

    def test_get_dataset_dimensions(self) -> None:
        # Invalid
        with self.assertRaises(requests.ConnectionError):
            self.invalid_connector.get_dataset_dimensions(VALID_ID_1)

        # Valid (note we only assigned dimensions to the test DATASET_1 during setUp())
        self.assertIsInstance(self.valid_connector.get_dataset_dimensions(VALID_ID_1), list)

    def test_assign_dimensions_to_dataset(self) -> None:
        # Invalid
        with self.assertRaises(requests.ConnectionError):
            self.invalid_connector.assign_dimensions_to_dataset(VALID_ID_2, VALID_DIMENSIONS)
        with self.assertRaises(TypeError):
            self.valid_connector.assign_dimensions_to_dataset(VALID_ID_2, "-")

        # Valid (and delete immediately after)
        self.assertTrue(self.valid_connector.assign_dimensions_to_dataset(VALID_ID_2, VALID_DIMENSIONS))
        self.valid_connector.session.delete(f'{self.valid_connector.client}/Datasets/'
                                            f'{VALID_ID_2}/dimensions', verify=False)


class TestNomisApiConnectorVariables(unittest.TestCase):
    def setUp(self) -> None:
        # Set up two connectors, one with a valid address and one without
        self.invalid_connector = NomisApiConnector(INVALID_CREDENTIALS, INVALID_ADDRESS)
        self.valid_connector = NomisApiConnector(VALID_CREDENTIALS, VALID_ADDRESS, PORT)

        # Create a variable to be used in the tests
        self.valid_connector.create_variable(VALID_VAR_NAME_1, VALID_VARIABLE_1)

    def tearDown(self) -> None:
        self.valid_connector.session.delete(f'{self.valid_connector.client}/Variables/{VALID_VAR_NAME_1}', verify=False)

    def test_variable_exists(self) -> None:
        # Invalid
        with self.assertRaises(requests.ConnectionError):
            self.invalid_connector.get_variable(VALID_VAR_NAME_1, return_bool=True)

        # Valid
        self.assertFalse(self.valid_connector.get_variable(VALID_VAR_NAME_2, return_bool=True))
        self.assertTrue(self.valid_connector.get_variable(VALID_VAR_NAME_1, return_bool=True))

    def test_create_variable(self) -> None:
        # Invalid
        with self.assertRaises(requests.ConnectionError):
            self.assertFalse(self.invalid_connector.create_variable(VALID_VAR_NAME_2, VALID_VARIABLE_2))
        with self.assertRaises(requests.HTTPError):
            self.valid_connector.create_variable(VALID_VAR_NAME_1, VALID_VARIABLE_2)
        with self.assertRaises(TypeError):
            self.valid_connector.create_variable(VALID_VAR_NAME_2, str(VALID_VARIABLE_2))

        # Valid
        self.assertTrue(self.valid_connector.create_variable(VALID_VAR_NAME_2, VALID_VARIABLE_2))
        # time.sleep(5)
        self.valid_connector.session.delete(f'{self.valid_connector.client}/Variables/{VALID_VAR_NAME_2}', verify=False)

    def test_get_variable_categories(self) -> None:
        with self.assertRaises(requests.ConnectionError):
            self.invalid_connector.get_variable_categories(VALID_VAR_NAME_1)
        with self.assertRaises(requests.ConnectionError):
            self.invalid_connector.get_variable_categories(VALID_VAR_NAME_2)
        self.assertIsInstance(self.valid_connector.get_variable_categories("GEOGRAPHY"), list)

    def test_create_variable_category(self) -> None:
        with self.assertRaises(requests.ConnectionError):
            self.invalid_connector.create_variable_category(VALID_VAR_NAME_1, VALID_CAT_ARR)
        with self.assertRaises(TypeError):
            self.valid_connector.create_variable_category(VALID_VAR_NAME_1, str(VALID_CAT_1))
        self.assertTrue(self.valid_connector.create_variable_category("GEOGRAPHY", VALID_CAT_ARR))
        # time.sleep(10)
        self.valid_connector.session.delete(f'{self.valid_connector.client}/Variables/GEOGRAPHY'
                                            f'/categories', verify=False)



if __name__ == '__main__':
    unittest.main()

