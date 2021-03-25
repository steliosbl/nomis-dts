from type_hints import *
from uuid import UUID
from api_connector import ApiConnector
import requests
import json
from logging import getLogger
logger = getLogger('DTS-Logger')

requests.packages.urllib3.disable_warnings() 

Metadata = Dict[str, Union[str, List[str]]]


class NomisMetadataApiConnector(ApiConnector):
    """
    Class for communicating directly with the Nomis metadata API; includes methods for retrieving metadata (by object
    or metadata ID), adding new/overwriting metadata, and updating existing metadata. This is the central hub of
    communication between the Nomis metadata API and the utility. It is easily extendable to contain more methods
    should the requirements change necessitating additional requests.
    """

    def __init__(self, credentials, address, port=None, record_requests=None) -> None:
        super().__init__(credentials, address, port, record_requests)
        logger.info(f"Establishing connection with the Nomis Metadata API at {self.client}.")

    @staticmethod
    def validate_uuid(id: str) -> bool:
        """
        Method for validating the id of a dataset.

        :raises TypeError: If the dataset's id is not a string.
        :raises ValueError: If the dataset is not in a valid uuid format.

        :return: `True` if the id is valid, otherwise an exception is raised.
        """
        if not isinstance(id, str):
            raise TypeError(f"The uuid of the dataset ({id}) is not a valid string.")

        try:
            UUID(id)
        except ValueError:
            raise ValueError(f"Dataset uuid ({id}) is not in a valid uuid format.")

        return True

    @staticmethod
    def validate_metadata(metadata: Union[List[Metadata], Metadata], id: str = None) -> bool:
        """
        Method for validating metadata, in terms of format and contents.

        :raises TypeError: If the metadata is not in the correct type (i.e., a Python dict), or if validate_uuid()
            detects a type error.
        :raises ValueError: If validate_uuid() detects a value error.

        :return: `True` if the metadata is valid, otherwise an exception is raised.
        """
        if not isinstance(metadata, (list, dict)):
            raise TypeError("Metadata in invalid format.")

        iter_md = [metadata] if isinstance(metadata, dict) else metadata
        for data in iter_md:
            if not isinstance(data, dict):
                raise TypeError("Metadata is invalid type, must be a Python dict.")

            if "id" in data and data["id"] is not None:
                NomisMetadataApiConnector.validate_uuid(data["id"])

            if "belongsTo" in data and data["belongsTo"] is not None:
                NomisMetadataApiConnector.validate_uuid(data["belongsTo"])

            if id is not None and ("id" not in data or id != data["id"]):
                raise ValueError("Metadata id does not match parameter id.")

        return True

    def get_all_metadata(self) -> List[Metadata]:
        """
        Method to retrieve all of the metadata on the server.

        :raises requests.ConnectionError: If an error occurs whilst attempting to communicate with the API.
        :raises requests.HTTPError: If a negative response is received from the API.

        :return: A list of metadata, if the request is a success; otherwise, an exception will have been raised.
        """
        # Attempt to retrieve the metadata associated with the ID
        try:
            res = self.session.get(f'{self.client}/Definitions', verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            logger.debug(f"SUCCESS: Metadata retrieved.")
            return res.json()
        elif res.status_code == 404:
            raise requests.HTTPError("Metadata not found")

    def get_metadata_for_object(self, id: str, return_bool: bool = False) -> Union[List[Metadata], bool]:
        """
        This takes a uuid representing the id of an object in the database as a parameter, and it makes a GET request
        to retrieve the metadata associated with this object.

        :param id: Valid string in uuid format representing the id of an object in the Nomis database.
        :param return_bool: Boolean toggle where, if set to True, will force the method to return a Boolean instead of
            the metadata.

        :raises requests.ConnectionError: If an error occurs whilst attempting to communicate with the API.
        :raises requests.HTTPError: If a negative response is received from the API.

        :return: The metadata for the object with the inputted id, if it exists; otherwise, an exception will be raised.
            Alternatively, if `return_bool` is set to `True`, return True if the metadata exists and False otherwise.
        """
        # Ensure the ID is a correct string
        self.validate_uuid(id)

        # Attempt to retrieve the metadata associated with the ID
        try:
            res = self.session.get(f'{self.client}/Content/{id}', verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            if return_bool:
                if len(res.json()) == 0:
                    logger.debug(f"Request successful, but there is no metadata for the object with ID {id}.")
                    return False
                else:
                    logger.debug(f"Metadata for object with id {id} retrieved.")
                    return True
            logger.debug(f"Metadata for object with ID {id} retrieved.")
            return res.json()
        else:
            if return_bool:
                logger.debug(f"Metadata for object with id {id} not found")
                return False
            raise requests.HTTPError(f"Metadata for object with id {id} not found.")

    def get_metadata_by_id(self, id: str, return_bool: bool = False) -> Union[Metadata, bool]:
        """
        This takes a uuid representing the id of some metadata in the database as a parameter, and makes a GET request
        to retrieve this metadata. NOTE that this is strictly distinct from the previous method: the uuid of metadata
        is not necessarily the same as the uuid of the object it represents (and some metadata represents no object).

        :param id: Valid string representing the ID of some metadata in the Nomis database.
        :param return_bool: Forces method to return True or False instead of returning the metadata or raising an
            exception in the case of a 200 or 404 response.

        :return: `False` if the id doesn't exist, is invalid, or has no associated metadata; the metadata, otherwise
        """
        try:
            # Ensure the ID is a correct string
            self.validate_uuid(id)

            # Attempt to retrieve the metadata associated with the ID
            try:
                res = self.session.get(f'{self.client}/Definitions/{id}', verify=False)
            except Exception as e:
                raise requests.ConnectionError(f"Unable to connect to client. ({e})")

            # Handle response
            if res.status_code == 200:
                if return_bool:
                    if len(res.json()) == 0:
                        logger.debug(f"There is no metadata with the ID {id}.")
                        return False
                    else:
                        logger.debug(f"Metadata with id {id} retrieved.")
                        return True
                logger.debug(f"Metadata with ID {id} retrieved.")
                return res.json()
            else:
                if return_bool:
                    return False
                raise requests.HTTPError(f"Metadata with id {id} not found")

        except (requests.ConnectionError, requests.HTTPError):
            logger.debug("ERROR: Unable to connect to the metadata API.")
        except Exception as e:
            logger.debug(f"ERROR: Unexpected error occurred when attempting to retrieve metadata by ID. ({str(e)})")
        return False

    def add_new_metadata(self, metadata: Union[List[Metadata]], return_uuids: bool = False) -> Union[List[str], bool]:
        """
        This takes an object representing an instance of Metadata and makes a POST request that adds this metadata to
        the server. This metadata is not required to have anything for its id: if it has no id then the API will
        generate a uuid for it automatically. If it does have an id, it must be in a valid uuid format, if not then the
        server will respond with an error (I have added a method to verify the uuid before the request is made). As a
        warning, the server will OVERWRITE any metadata on the server that has the same id as what is being posted.
        Therefore, calling the get_metadata_by_id() method prior to this method is worthwhile to check whether we will
        or won't overwrite anything by calling this method. This method returns the uuid of the metadata that was
        appended to the server.

        :param metadata: Valid list of dictionary of strings representing metadata.
        :param return_uuids: Toggle for returning uuids instead of a boolean confirmation - for testing purposes.

        :return: Bool indicating the success of the request, or the ids of the appended datasets if toggled for.
        """
        # Establish headers
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

        # Ensure the metadata is a correct dict instance
        self.validate_metadata(metadata)

        # Attempt to retrieve the metadata associated with the ID
        try:
            res = self.session.post(f'{self.client}/Definitions',
                                    data=json.dumps(metadata), headers=headers, verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            logger.debug(f"SUCCESS: New metadata added successfully")
            if return_uuids:
                ids = []
                for ds in res.json():
                    ids.append(ds['id'])
                return ids
            return True
        elif res.status_code == 400:
            raise requests.HTTPError(f"Unable to add new metadata due to validation errors. ({res.text})")
        elif res.status_code == 409:
            raise requests.HTTPError(f"ERROR: Unable to add new metadata due to conflict.")
        else:
            raise requests.HTTPError(f"Unexpected status code: {res.status_code}. ({res.text})")

    def update_metadata_association(self, id: str, metadata: Metadata) -> bool:
        """
        As above, this method takes an instance of Metadata as a parameter, but it also requires a valid uuid as an
        additional parameter. This method entails making a PUT request that will update any existing metadata, or create
        some new metadata if the id does not exist on the server. The metadata object here can be "incomplete", in which
        case it will only update the included fields upon making the request; however, the metadata must have a valid
        id, and this id must match the one passed to the method in the parameters.

        :param id: Valid string representing the ID of some metadata in the Nomis database.
        :param metadata: Valid dictionary of strings representing metadata attributes (must include belongsTo).
        :return: Bool indicating the success of the request.
        """
        # Establish headers
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

        # Ensure the ID is a correct string and the metadata is a correct dict instance
        self.validate_uuid(id)
        self.validate_metadata(metadata, id)

        if "belongsTo" not in metadata or metadata['belongsTo'] is None:
            belongs_to = ""
        else:
            belongs_to = f" for object with ID {metadata['belongsTo']}"

        # Attempt to retrieve the metadata associated with the ID
        try:
            res = self.session.put(f'{self.client}/Definitions/{id}',
                                   data=json.dumps(metadata), headers=headers, verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 201:
            logger.debug(f"Metadata with ID {id}{belongs_to} successfully updated.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError(f"Unable to update metadata with ID {id}{belongs_to} due to a bad request.")
        elif res.status_code == 409:
            raise requests.HTTPError(f"ERROR: Unable to update metadata with ID {id}{belongs_to} due to conflict.")
        else:
            raise requests.HTTPError(f"Unexpected status code: {res.status_code}. ({res.text})")
