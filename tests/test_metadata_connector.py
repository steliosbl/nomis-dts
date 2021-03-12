import unittest.mock
import uuid
from nomis_metadata_api_connector import NomisMetadataApiConnector
"""
To run:
 - The metadata API must be running locally 

Test all:
 - python test_metadata_connector.py -b

Test individual cases:
 - python -m unittest test_metadata_connector.TestMetadataConnector.[TEST CASE]
for instance,
 - python -m unittest test_metadata_connector.TestMetadataConnector.test_get_metadata_for_object
 - python -m unittest test_metadata_connector.TestMetadataConnector.test_get_metadata_by_id
 - python -m unittest test_metadata_connector.TestMetadataConnector.test_add_new_metadata
 - python -m unittest test_metadata_connector.TestMetadataConnector.test_update_metadata_association

"""

VALID_ADDRESS = 'https://localhost'
VALID_CREDENTIALS = ('a', 'b')
VALID_PORT = '5001'
VALID_OBJECT_ID = "7b9568e3-019e-4faf-8a50-98c66332ba09"


VALID_METADATA = {
  "belongsTo": str(uuid.uuid4()),
  "description": "test",
  "created": "2021-02-24T14:14:32.202Z",
  "validFrom": "2021-02-24T14:14:32.202Z",
  "validTo": "2021-02-24T14:14:32.202Z",
  "include": [
    "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  ],
  "meta": [
    {
      "role": "string",
      "properties": [
        {
          "prefix": "string",
          "property": "string",
          "value": "string"
        }
      ]
    }
  ]
}

# todo: add invalid cases


class TestMetadataConnector(unittest.TestCase):
    def setUp(self) -> None:
        self.headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        self.obj_id = VALID_METADATA["belongsTo"]
        self.valid_connector = NomisMetadataApiConnector(('a', 'b'), "https://localhost", '5001')
        self.uuid = self.valid_connector.add_new_metadata(VALID_METADATA)

    def tearDown(self) -> None:
        self.valid_connector.session.delete(f"{self.valid_connector.client}/Definitions/{self.uuid}", verify=False)
    
    def test_get_metadata_for_object(self):
        self.assertTrue(self.valid_connector.get_metadata_for_object(self.obj_id), True)

    def test_get_metadata_by_id(self):
        self.assertIsInstance(self.valid_connector.get_metadata_by_id(self.uuid), dict)
    
    def test_add_new_metadata(self):
        this_uuid = self.valid_connector.add_new_metadata(VALID_METADATA)
        self.assertIsInstance(this_uuid, str)
        self.valid_connector.session.delete(f"{self.valid_connector.client}/Definitions/{this_uuid}", verify=False)
        
    def test_update_metadata_association(self):
        # Test updating
        update_md = {"id": self.uuid, "belongsTo": self.obj_id, "description": "updated"}
        self.assertTrue(self.valid_connector.update_metadata_association(self.uuid, update_md))
        ret_md = self.valid_connector.get_metadata_by_id(self.uuid)
        self.assertEqual(ret_md["description"], "updated")

        # Revert back (and test)
        update_md = {"id": self.uuid, "belongsTo": self.obj_id, "description": "test"}
        self.assertTrue(self.valid_connector.update_metadata_association(self.uuid, update_md))
        ret_md = self.valid_connector.get_metadata_by_id(self.uuid)
        self.assertEqual(ret_md["description"], "test")


if __name__ == "__main__":
    unittest.main()
