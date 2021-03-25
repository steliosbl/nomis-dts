import sys; sys.path.append('..')
import unittest
from dataset_transformations import DatasetTransformations
from collections import OrderedDict
from type_hints import *
from pyjstat import pyjstat

"""
Prerequisite:
  - None

Test all:        
 - python test_dataset_transformations.py 

To run specific tests:   
 - python -m unittest test_dataset_transformations.TestDatasetTransformations.[test]
for instance,
 - python -m unittest test_dataset_transformations.TestDatasetTransformations.test_validate_table
 - python -m unittest test_dataset_transformations.TestDatasetTransformations.test_category_creation

Note: include -b flag to silence stdout

"""


VALID_TABLE = pyjstat.Dataset([
    ('version', '2.0'),
    ('class', 'dataset'),
    ('source', 'Usual Residents: England and Wales'),
    ('updated', '2021-02-13T01:15:59Z'),
    ('id', ['SEX']),
    ('size', [2]),
    ('dimension', OrderedDict([
        ('SEX', OrderedDict([
            ('label', 'Sex'),
            ('category', OrderedDict([
                ('index', ['1', '2']),
                ('label', OrderedDict([
                    ('1', 'Male'),
                    ('2', 'Female')
                ]))
            ]))
        ]))
    ])),
    ('extension', OrderedDict([
        ('cantabular', OrderedDict([
            ('dataset', OrderedDict([
                ('name', 'Usual-Residents'),
                ('digest', 'c932e250328b1cb6083ad580e9cc4ed6e3d7d3073ae8295b7589c8914bd5c834')
            ])),
            ('blocked', None)
        ]))
    ])),
    ('value', [27517574, 28421312])
])

INVALID_TABLE = pyjstat.Dataset([
    ('version', '2.0'),
    ('class', 'dataset'),
    ('source', 'Usual Residents: England and Wales'),
    ('updated', '2021-02-13T01:15:59Z'),
    ('id', ['SEX']),
    ('size', [2]),
    ('extension', OrderedDict([
        ('cantabular', OrderedDict([
            ('dataset', OrderedDict([
                ('name', 'Usual-Residents'),
                ('digest', 'c932e250328b1cb6083ad580e9cc4ed6e3d7d3073ae8295b7589c8914bd5c834')
            ])),
            ('blocked', None)
        ]))
    ])),
    ('value', [27517574, 28421312])
])

VALID_ID = "DATASET_ID"
VALID_TITLE = "DATASET_TITLE"

VALID_UUID_MD = UuidMetadata(
    uuid='60742e2e-b54d-4cd6-adfa-fc2adc98fe24', 
    metadata={
        'description': 'Test metadata.'
    }
)


class TestDatasetTransformations(unittest.TestCase):

    def setUp(self) -> None:
        """Set up a valid instance of DatasetTransformation."""
        self.valid_dataset_transformations = DatasetTransformations(VALID_TABLE)

    def test_validate_table(self):
        """Test that an instance of DataTransformations is blocked when the table parameter is invalid
        """
        with self.assertRaises(LookupError):
            DatasetTransformations(INVALID_TABLE)
        with self.assertRaises(TypeError):
            DatasetTransformations({"dimensions": True})

    def test_dataset_creation(self) -> None:
        """Test the dataset_creation() method of the DatasetTransformations class by asserting that expected exceptions
        are raised on invalid parameters, and that on valid calls all returned values and types are as expected. Also 
        ensure that the method works as a staticmethod, i.e. is callable without creating an instance of the class.
        """
        # Ensure expected exceptions are raised upon invalid parameters
        with self.assertRaises(TypeError):
            self.valid_dataset_transformations.dataset_creation(VALID_ID, 42)
        with self.assertRaises(ValueError):
            self.valid_dataset_transformations.dataset_creation("", VALID_TITLE)

        # Retrieve a dataset using valid strings as the dataset title and id
        ds = self.valid_dataset_transformations.dataset_creation(VALID_ID, VALID_TITLE)

        # Ensure use as a staticmethod works in the same way
        self.assertEqual(ds, DatasetTransformations.dataset_creation(VALID_ID, VALID_TITLE))

        # Value & Type check
        self.assertIsInstance(ds, dict)
        self.assertEqual(ds["id"], VALID_ID)
        self.assertEqual(ds["title"], VALID_TITLE)

    def test_variable_creation(self) -> None:
        """Test the variable_creation() method of the DatasetTransformations class by assuring that on the valid
        instances all types and values are as expected
        """
        # Retrieve variables using the valid pyjstat table and assert types/values are as expected
        varis = self.valid_dataset_transformations.variable_creation()
        self.assertIsInstance(varis, list)
        for var in varis:
            self.assertIsInstance(var, dict)
            self.assertTrue(var["name"] in self.valid_dataset_transformations.table["dimension"])

    def test_category_creation(self) -> None:
        """Test the category_creation() method
        """
        # Check valid attempts
        cats = self.valid_dataset_transformations.category_creation(["10000"])
        self.assertIsInstance(cats, list)
        for cat in cats:
            self.assertIsInstance(cat, dict)

    def test_assign_dimensions(self) -> None:
        """Test the assign_dimensions() method
        """
        dims = self.valid_dataset_transformations.assign_dimensions("SEX")
        self.assertIsInstance(dims, list)
        for dim in dims:
            self.assertIsInstance(dim, dict)

    def test_observations(self) -> None:
        """Test the observations() method
        """
        with self.assertRaises(TypeError):
            self.valid_dataset_transformations.observations(12345)
        with self.assertRaises(ValueError):
            self.valid_dataset_transformations.observations("")
        obs = self.valid_dataset_transformations.observations(VALID_ID)
        self.assertIsInstance(obs, dict)
        self.assertEqual(obs["dataset"], VALID_ID)

    def test_variable_metadata_request(self):
        """Test the variable_metadata_request() method
        """
        with self.assertRaises(TypeError):
            self.valid_dataset_transformations.variable_metadata_request(VALID_UUID_MD)
        mds = self.valid_dataset_transformations.variable_metadata_request([VALID_UUID_MD])
        self.assertIsInstance(mds, list)
        for md in mds:
            self.assertIsInstance(md, dict)
            self.assertEqual(md['belongsTo'], VALID_UUID_MD.uuid)


if __name__ == "__main__":
    unittest.main()
