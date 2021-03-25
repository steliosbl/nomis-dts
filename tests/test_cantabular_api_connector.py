import sys; sys.path.append('..')
import unittest
import requests
from pyjstat import pyjstat
from cantabular_api_connector import CantabularApiConnector

"""
Prerequisites:
 - The Cantabular API server must be operational
 
To run all tests:
 - python test_cantabular_api_connector.py
 
To run specific tests:   
 - python -m unittest test_cantabular_api_connector.TestCantabularApiConnector.[test]
for instance,
 - python -m unittest test_cantabular_api_connector.TestCantabularApiConnector.test_valid_dataset
 - python -m unittest test_cantabular_api_connector.TestCantabularApiConnector.test_invalid_dataset

Note: include -b flag to silence stdout
"""

VALID_DATASET = 'Usual-Residents'
INVALID_DATASET = 'Not-a-Dataset'
VALID_QUERY_VARS_1 = ['SEX']
VALID_QUERY_VARS_2 = ['COUNTRY', 'AGE']
INVALID_QUERY_VARS = ['NOT', 'REAL']
VALID_ADDRESS = "https://ftb-api-ext.ons.sensiblecode.io"
VALID_CREDENTIALS = ('durham.project', 'extra.carrot.slowly')
INVALID_CREDENTIALS = ('nietzsche.horse', 'friedrich.turin')


class TestCantabularApiConnector(unittest.TestCase):

    def test_valid_dataset(self):
        with CantabularApiConnector(VALID_DATASET, VALID_QUERY_VARS_1, VALID_CREDENTIALS, VALID_ADDRESS) as con:
            self.assertIsInstance(con.query(), pyjstat.Dataset)
        with CantabularApiConnector(VALID_DATASET, VALID_QUERY_VARS_2, VALID_CREDENTIALS, VALID_ADDRESS) as con:
            self.assertIsInstance(con.query(), pyjstat.Dataset)

    def test_invalid_dataset(self):
        with self.assertRaises(requests.HTTPError):
            with CantabularApiConnector(INVALID_DATASET, VALID_QUERY_VARS_1, VALID_CREDENTIALS, VALID_ADDRESS) as con:
                con.query()
        with self.assertRaises(requests.HTTPError):
            with CantabularApiConnector(INVALID_DATASET, VALID_QUERY_VARS_2, VALID_CREDENTIALS, VALID_ADDRESS) as con:
                con.query()

    def test_invalid_variables(self):
        with self.assertRaises(requests.HTTPError):
            with CantabularApiConnector(VALID_DATASET, INVALID_QUERY_VARS, VALID_CREDENTIALS, VALID_ADDRESS) as con:
                con.query()

    def test_bad_connection(self):
        with self.assertRaises(requests.ConnectionError):
            with CantabularApiConnector(VALID_DATASET, VALID_QUERY_VARS_1, VALID_CREDENTIALS, "fake.address") as con:
                con.query()

    def test_unauthorised(self):
        with self.assertRaises(requests.HTTPError):
            with CantabularApiConnector(VALID_DATASET, VALID_QUERY_VARS_1, INVALID_CREDENTIALS, VALID_ADDRESS) as con:
                con.query()


if __name__ == '__main__':
    unittest.main()
