import io
import unittest
import uuid
from unittest.mock import patch
from cantabular_client import Table, AuthenticationError
from cantabular_api_connector import CantabularApiConnector
from variable import Variable
from variable_category import VariableCategory
from assign_dimensions import AssignDimensions
from dataset_observations import DatasetObservations
from dataset_creation import DatasetCreation


VALID_CREDENTIALS = ("durham.project", "extra.carrot.slowly")
INVALID_CREDENTIALS = ("bad.user", "bad.pass")
INVALID_CREDENTIALS2 = ("not.a.user")
VALID_URL = 'https://ftb-api-ext.ons.sensiblecode.io'
INVALID_URL = 'https://badurl'
VALID_QUERY_DS = 'Usual-Residents'
VALID_QUERY_VARIABLES = ['COUNTRY', 'HEALTH_T004A', 'SEX']
INVALID_QUERY_VARIABLES = {'COUNTRY', 'HEALTH_T004A', 'SEX'}


# Note: been getting "access denied" on Cantabular so unable to properly test,
# but this should be correctly testing for the expected functionality

class TestCantabularConnector(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_connector = CantabularApiConnector(VALID_URL, VALID_CREDENTIALS)
        self.connector_invalid_creds = CantabularApiConnector(VALID_URL, INVALID_CREDENTIALS)
        self.connector_invalid_url = CantabularApiConnector(INVALID_URL, VALID_CREDENTIALS)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_query_isvalid(self, mock_stdout) -> None:
        self.assertIsInstance(self.valid_connector.query(VALID_QUERY_DS, VALID_QUERY_VARIABLES), Table)
        if self.valid_connector.blocked_categories:
            RULE_VAR_NAME, RULE_VAR = list(self.valid_connector.blocked_categories.items())[0]
            s = f'The following categories of {RULE_VAR_NAME} failed disclosure control checks:\n'
            s += ', '.join(RULE_VAR['category']['label'].values())
            s += '\n'
            self.assertEqual(mock_stdout.getvalue(), s)

    def test_connection_invalid(self) -> None:
        with self.assertRaises(Exception):
            self.valid_connector.query(VALID_QUERY_DS, INVALID_QUERY_VARIABLES)
            self.connector_invalid_url.query(VALID_QUERY_DS, VALID_QUERY_VARIABLES)
            self.connector_invalid_creds.query(VALID_QUERY_DS, VALID_QUERY_VARIABLES)
            CantabularApiConnector(VALID_URL, INVALID_CREDENTIALS2)


class TestDataProcessorCluster(unittest.TestCase):
    def setUp(self) -> None:
        valid_connector = CantabularApiConnector(VALID_URL, VALID_CREDENTIALS)
        self.valid_table = valid_connector.query(VALID_QUERY_VARIABLES, VALID_QUERY_DS)
        self.a_uuid = str(uuid.uuid4())

    def test_valid_variable(self) -> None:
        valid_variable = Variable(self.valid_table)
        valid_variable_request = valid_variable.variable_requests()
        self.assertIsInstance(valid_variable_request, list)
        self.assertIn("name", valid_variable_request[0])
        self.assertIn("label", valid_variable_request[0])
        self.assertIn("metadata", valid_variable_request[0])
        self.assertIn("defaults", valid_variable_request[0])

    def test_invalid_variable(self) -> None:
        with self.assertRaises(Exception):
            invalid_variable = Variable({'not': 'valid'})
            invalid_variable.variable_requests()

    def test_valid_variable_category(self):
        valid_variable_category = VariableCategory(self.valid_table)
        self.assertIsInstance(valid_variable_category.category_requests(), list)

    def test_invalid_variable_category(self):
        with self.assertRaises(Exception):
            invalid_variable_category = VariableCategory({'not': 'valid'})
            invalid_variable_category.category_requests()

    def test_valid_assign_dimensions(self):
        valid_assign_dimensions = AssignDimensions(self.valid_table)
        valid_dimensions = valid_assign_dimensions.assign_dimensions_requests()
        self.assertIsInstance(valid_dimensions, dict)
        self.assertTrue(len(valid_dimensions) != 0)

    def test_invalid_assign_dimensions(self):
        with self.assertRaises(Exception):
            invalid_assign_dimensions = AssignDimensions({'not': 'valid'})
            invalid_assign_dimensions.assign_dimensions_requests()

    def test_valid_dataset_observations(self):
        valid_dataset_observations = DatasetObservations({'not': 'valid'}, self.a_uuid)
        valid_observations = valid_dataset_observations.observations_request()
        self.assertIsInstance(valid_observations, list)
        self.assertTrue(len(valid_observations) != 0)

    def test_invalid_dataset_observations(self):
        with self.assertRaises(Exception):
            invalid_dataset_observations = DatasetObservations({'not': 'valid'}, self.a_uuid)
            invalid_dataset_observations.observations_request()

    def test_valid_dataset_creation(self):
        valid_dataset_creation = DatasetCreation(self.a_uuid, "ds_title")
        valid_dataset = valid_dataset_creation.dataset_request()
        self.assertIsInstance(valid_dataset, dict)
        self.assertIn("id", valid_dataset)
        self.assertIn("title", valid_dataset)
        self.assertIn("contactId", valid_dataset)
        self.assertIn("isAdditive", valid_dataset)
        self.assertIn("isFlagged", valid_dataset)
        self.assertIn("derivedFrom", valid_dataset)
        self.assertIn("restrictedAccess", valid_dataset)
        self.assertIn("minimumRound", valid_dataset)
        self.assertIn("online", valid_dataset)
        self.assertEqual(valid_dataset["id"], self.a_uuid)
        self.assertEqual(valid_dataset["title"], "ds_title")

    def test_invalid_dataset_creation(self):
        with self.assertRaises(Exception):
            invalid_dataset_creation = DatasetCreation("01100", "ds_title")
            invalid_dataset_creation.dataset_request()


if __name__ == '__main__':
    unittest.main()
