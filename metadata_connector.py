from typing import Union, Tuple, Dict, List, Any
from type_hints import *
from uuid import UUID
import requests
import json

requests.packages.urllib3.disable_warnings() 

Metadata = Dict[str, Union[str, List[str]]]

"""
INFO

Some of the class methods will likely be removed as they are non-essential, but for the sake of testing I incorporated 
methods for most of the requests that it is possible to make to the Nomis metadata server. The methods are as follows:

 - get_all_metadata()
    -> This does as it's name suggests: it simply retrieves all of the metadata on the server. This is almost certainly
       not a method we will require, but I implemented it anyway when I was first getting to grips with the API.
       
 - get_metadata_for_object()
    -> This takes a uuid representing the id of an object in the database as a parameter, and it makes a GET request to
       retrieve the metadata associated with this object.
 
 - get_metadata_by_id()
    -> This takes a uuid representing the id of some metadata in the database as a parameter, and makes a GET request to 
       retrieve this metadata. 
    -> NOTE that this is strictly distinct from the previous method: the uuid of metadata is not necessarily the same as
       the uuid of the object it represents (and some metadata represents no object).

 - add_new_metadata()
    -> This takes an object representing an instance of Metadata (see the type definition above) and makes a POST 
       request that adds this metadata to the server. This metadata is not required to have anything for its id: if it 
       has no id then the API will generate a uuid for it automatically. If it does have an id, it must be in a valid 
       uuid format, if not then the server will respond with an error (I have added a method to verify the uuid before 
       the request is made). As a warning, the server will OVERWRITE any metadata on the server that has the same id as
       what is being posted. Therefore, calling the get_metadata_by_id() method prior to this method is worthwhile to 
       check whether we will or won't overwrite anything by calling this method.
    -> This method returns the uuid of the metadata that was appended to the server.
       
 - update_metadata_association() 
    -> As above, this method takes an instance of Metadata as a parameter, but it also requires a valid uuid as an 
       additional parameter. This method entails making a PUT request that will update any existing metadata, or create
       some new metadata if the id does not exist on the server. The metadata object here can be "incomplete", in which 
       case it will only update the included fields upon making the request; however, the metadata must have a valid 
       id, and this id must match the one passed to the method in the parameters.
"""


class NomisMetadataApiConnector:
    def __init__(self, address: str, credentials: Tuple[str, str], port: Union[str, None] = "5001") -> None:
        """
        :param address:
        :type address:

        :param credentials:
        :type credentials:

        :param port:
        :type port:
        """
        self.client = f"{str(address)}:{str(port)}" if port is not None else str(address)
        self.session = requests.Session()  # Begin a session
        self.session.auth = credentials

    def __enter__(self) -> 'NomisMetadataApiConnector':
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        requests.Session.close(self.session)

    def validate_metadata(self) -> bool:
        # assert
        pass

    def get_all_metadata(self) -> Union[List[Metadata], bool]:
        try:
            # Attempt to retrieve the metadata associated with the ID
            res = self.session.get(f'{self.client}/Definitions', verify=False)

            # Handle response
            if res.status_code == 200:
                print(f"SUCCESS: Metadata retrieved.")
                return res.json()
            elif res.status_code == 404:
                print("ERROR: Metadata not found")
                return False

        except (requests.ConnectionError, requests.HTTPError):
            print("ERROR: Unable to connect to the metadata API.")
        except Exception as e:
            print(f"ERROR: Unexpected error occurred when attempting to retrieve all metadata. ({str(e)})")
        return False

    def get_metadata_for_object(self, id: str) -> Union[List[Metadata], bool]:
        """
        id:       Valid string representing the ID of an object in the Nomis database
        return:   False if the id doesn't exist, is invalid, or has no associated metadata; the metadata, otherwise
        """
        try:
            # Ensure the ID is a correct string
            if not isinstance(id, str):
                print("Invalid ID")
                return False
            try:
                UUID(id)
            except ValueError:
                print("ERROR: ID passed is not a valid UUID.")
                return False

            # Attempt to retrieve the metadata associated with the ID
            res = self.session.get(f'{self.client}/Content/{id}', verify=False)

            # Handle response
            if res.status_code == 200:
                if len(res.json()) == 0:
                    print(f"SUCCESS: There is no metadata for the object with ID {id}.")
                    return False
                print(f"SUCCESS: Metadata for object with ID {id} retrieved.")
                return True  # res.json()
            else:
                print("ERROR: Metadata not found")
                return False

        except (requests.ConnectionError, requests.HTTPError):
            print("ERROR: Unable to connect to the metadata API.")
        except Exception as e:
            print(f"ERROR: Unexpected error occurred when attempting to retrieve metadata for an object. ({str(e)})")
        return False

    def get_metadata_by_id(self, id: str) -> Union[Metadata, bool]:
        """
        id:       Valid string representing the ID of some metadata in the Nomis database
        return:   False if the id doesn't exist, is invalid, or has no associated metadata; the metadata, otherwise
        """
        try:
            # Ensure the ID is a correct string
            if not isinstance(id, str):
                print("ERROR: ID is not a valid string.")
                return False
            try:
                UUID(id)
            except ValueError:
                print("ERROR: ID passed is not a valid UUID.")
                return False

            # Attempt to retrieve the metadata associated with the ID
            res = self.session.get(f'{self.client}/Definitions/{id}', verify=False)

            # Handle response
            if res.status_code == 200:
                if len(res.json()) == 0:
                    print(f"There is no metadata with the ID {id}.")
                    return True
                print(f"SUCCESS: Metadata with ID {id} retrieved.")
                return res.json()
            else:
                print("ERROR: Metadata not found")
                return False

        except (requests.ConnectionError, requests.HTTPError):
            print("ERROR: Unable to connect to the metadata API.")
        except Exception as e:
            print(f"ERROR: Unexpected error occurred when attempting to retrieve metadata by ID. ({str(e)})")
        return False

    def add_new_metadata(self, metadata: Metadata) -> Union[str, bool]:
        """
        metadata: Valid dictionary of strings representing metadata
        return:   Bool indicating the success of the request
        """
        try:
            # Establish headers
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

            # Ensure the metadata is a correct dict instance
            if not isinstance(metadata, list):
                print("ERROR: Metadata in invalid format.")
                return False
            if "id" in metadata and metadata["id"] is not None:
                try:
                    UUID(metadata["id"])
                except ValueError:
                    print("ERROR: ID in input metadata is not a valid UUID.")
                    return False

            if "belongsTo" not in metadata or metadata['belongsTo'] is None:
                belongs_to = ""
            else:
                belongs_to = f" for object with ID {metadata['belongsTo']}"

            # Attempt to retrieve the metadata associated with the ID
            res = self.session.post(f'{self.client}/Definitions',
                                    data=json.dumps(metadata), headers=headers, verify=False)

            # Handle response
            if res.status_code == 200:
                print(f"SUCCESS: New metadata added successfully")
                return True
            elif res.status_code == 400:
                print(f"ERROR: Unable to add new metadata due to validation errors.")
                print(res.json())
                return False
            elif res.status_code == 409:
                print(f"ERROR: Unable to add new metadata due to conflict.")
                print(res.json())
                return False
            else:
                print("Unexpected status code: ", res.status_code)
                print(res.json())

        except (requests.ConnectionError, requests.HTTPError):
            print("ERROR: Unable to connect to the metadata API.")
        except Exception as e:
            print(f"ERROR: Unexpected error occurred when trying to add some new metadata. ({str(e)})")
        return False

    def update_metadata_association(self, id: str, metadata: Metadata) -> bool:
        """
        id:       Valid string representing the ID of some metadata in the Nomis database
        metadata: Valid dictionary of strings representing metadata attributes (must include belongsTo)
        return:   Bool indicating the success of the request
        """
        try:
            # Establish headers
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

            # Ensure the ID is a correct string and the metadata is a correct dict instance
            if not isinstance(id, str):
                print("ERROR: ID is not a valid string.")
                return False
            if not isinstance(metadata, dict):
                print("ERROR: Metadata in invalid format.")
                return False

            if "id" not in metadata:
                print("ERROR: Metadata must contain an id key.")
                return False
            elif metadata["id"] != id:
                print("ERROR: Metadata id does not match parameter id.")
                return False
            try:
                UUID(metadata["id"])
            except ValueError:
                print("ERROR: ID in input metadata is not a valid UUID.")
                return False

            if "belongsTo" not in metadata or metadata['belongsTo'] is None:
                belongs_to = ""
            else:
                belongs_to = f" for object with ID {metadata['belongsTo']}"

            # Attempt to retrieve the metadata associated with the ID
            res = self.session.put(f'{self.client}/Definitions/{id}',
                                   data=json.dumps(metadata), headers=headers, verify=False)

            # Handle response
            if res.status_code == 201:
                print(f"SUCCESS: Metadata with ID {id}{belongs_to} successfully updated.")
                print(res.json())
                return True
            elif res.status_code == 400:
                print(f"ERROR: Unable to update metadata with ID {id}{belongs_to} due to a bad request.")
                print(res.json())
                return False

            elif res.status_code == 409:
                print(f"ERROR: Unable to update metadata with ID {id}{belongs_to} due to conflict.")
                print(res.json())
                return False
            else:
                print("Unexpected status code: ", res.status_code)
                print(res.json())

        except (requests.ConnectionError, requests.HTTPError):
            print("ERROR: Unable to connect to the metadata API.")
        except Exception as e:
            print(f"ERROR: Unexpected error occurred when add some new metadata. ({str(e)})")
        return False


md = {
  "id": "2a570a0c-8f07-4f4d-8730-b36259428ac0",
  # "belongsTo": "7b9568e3-019e-4faf-8a50-98c66332bb09",
  "description": "UPDATE",
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


# new = NomisMetadataApiConnector("https://localhost", ('a', 'b'), '5001')
# this = new.get_all_metadata()
# this = new.get_metadata_for_object("2dc382c4-a0d9-46cf-9ce4-60d045a6498a")
# this = new.get_metadata_by_id("ea35c6ef-2c4c-4a81-9706-4337a5d31d70")
# this = new.add_new_metadata(md)
# this = new.update_metadata_association("2a570a0c-8f07-4f4d-8730-b36259428ac0", md)
# print(this)
