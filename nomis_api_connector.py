import requests
import json
from type_hints import *
from uuid import UUID
from api_connector import ApiConnector
from logging import getLogger
logger = getLogger('DTS-Logger')


requests.packages.urllib3.disable_warnings() 


class NomisApiConnector(ApiConnector):
    """API Connector class for communicating with Nomis' main API. Provides the functionality of appending and altering
    datasets and variables on the Nomis database through the Nomis API.
    """
    def __init__(self, credentials, address, port=None) -> None:
        super().__init__(credentials, address, port)

    @staticmethod
    def validate_ds(ds: NomisDataset, id: str = None) -> bool:
        """Method for validating that a dataset is in the correct format and contains the required information.
        Validation is done simply by first ensuring the dataset is the correct type (a Python dict), and then by
        checking the individual keys in the dataset, ensuring they are all in the correct type and format, and if they
        aren't optional that they exist in the first place.

        :param ds: A dictionary representing a dataset ready to be transmitted to the Nomis server.
        :param id: Optionally, can include an id to verify that parameter id matches that of dataset

        :raises TypeError: If the dataset itself or any of its elements are of an incorrect type.
        :raises KeyError: If the dataset is missing elements or has unexpected ones.
        :raises ValueError: If the dataset contains an uuid and it isn't in a valid UUID format.

        :return: If an exception isn't raised, the method will return True.
        """
        # Validate dataset types and keys
        try:
            if not isinstance(ds, dict):
                raise TypeError("ERROR: Dataset is not a valid Python dict.")

            if not isinstance(ds["id"], str):
                raise TypeError("ERROR: Dataset id is not a valid string.")

            if not isinstance(ds["title"], str):
                raise TypeError("ERROR: Dataset title is not a valid string.")

            if ds["contactId"] is not None and not isinstance(ds["contactId"], str):
                raise TypeError("ERROR: Dataset contactId is not a valid string.")

            if not isinstance(ds["isAdditive"], bool):
                raise TypeError("ERROR: Dataset isAdditive is not a valid string.")

            if not isinstance(ds["isFlagged"], bool):
                raise TypeError("ERROR: Dataset isFlagged is not a valid string.")

            if ds["derivedFrom"] is not None and not isinstance(ds["derivedFrom"], str):
                raise TypeError("ERROR: Dataset derivedFrom is not a valid string.")

            if not isinstance(ds["restrictedAccess"], bool):
                raise TypeError("ERROR: Dataset restrictedAccess is not a bool.")

            if not isinstance(ds["online"], bool):
                raise TypeError("ERROR: Dataset online is not a bool.")

            if len(ds) > 13:
                raise KeyError

        except KeyError:
            raise KeyError("ERROR: Dataset has missing or invalid keys.")

        # Ensure dataset UUID, if it has one, is in a valid uuid format
        try:
            UUID(ds["uuid"])

        except ValueError:
            raise ValueError("ERROR: Dataset UUID is not a valid UUID.")

        except KeyError:
            pass

        if id is not None and not ds["id"] == id:
            raise ValueError("Dataset ID does not match parameter ID.")

        # This will be reached if and only if no exceptions are raised, indicating a valid dataset
        logger.info(f"SUCCESS: Dataset with {ds['id']} validated.")
        return True

    @staticmethod
    def validate_id(id: str) -> bool:
        """Method for validating parameter IDs

        :param id: A string that is in a valid ID format.

        :raises TypeError: If the inputted id is not a string.
        :raises ValueError: If the inputted id is not in the correct format.

        :return: True if the id is valid, otherwise an exception is raised
        """
        if not isinstance(id, str):
            raise TypeError("Invalid id, must be a string.")

        if len(id) == 0:
            raise ValueError("Id passed is not in a valid format.")

        return True

    # GET | PUBLIC
    def get_dataset(self, id: str, return_bool: bool = False) -> Union[NomisDataset, bool]:
        """Method for obtaining a dataset from the Nomis database by its uuid. Makes a GET request to the Nomis API
        at the /Datasets/{id} endpoint, and returns the dataset if the response code is 200; otherwise, an appropriate
        exception is raised. Alternatively, if the return_bool param is set to True, this method will simply check for
        the existence of a dataset and return a Boolean response.

        :param id: A string that is in a valid ID format.
        :param return_bool: Admin parameter; returns True or False instead of returning the dataset or raising
        exception in the case of a 200 or 404 response.

        :raises TypeError: If the validate_id() method detects that the id is not a string.
        :raises ValueError: If the validate_id() method detects that the dataset uuid is not in the correct UUID format.
        :raises requests.HTTPError: If either connecting to the API is unsuccessful or a negative response is received.

        :return: If the request is successful, then return the dataset associated with the inputted ID. Alternatively,
        if return_bool=True, return True if dataset exists, else False
        """
        # Type/value checking
        self.validate_id(id)

        # Make the request: Get dataset definition.
        try:
            res = self.session.get(
                f'{self.client}/Datasets/{id}',
                verify=False
            )
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        # If the dataset exists, the response code will be 200; other responses correspond to the API documentation.
        if res.status_code == 200:
            if return_bool:
                logger.info(f"Dataset with id '{id}' exists.")
                return True

            logger.info("Dataset found.")
            return res.json()

        elif res.status_code == 400:
            raise requests.HTTPError("Bad input parameter.")

        elif res.status_code == 404:
            if return_bool:
                logger.info(f"Dataset with id '{id}' does not exist.")
                return False

            raise requests.HTTPError(f"Dataset (id: {id}) not found.")

        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # PUT | DATASET-ADMIN - WILL REQUIRE AUTH.
    def create_dataset(self, id: str, ds: NomisDataset) -> bool:
        """Method for uploading a dataset to the Nomis database. Makes a PUT request to the /Datasets/{id} endpoint,
        with a valid Dataset object encoded into JSON as the body. True is returned by the method if the dataset
        creation is successful (i.e., a 200 code is received), otherwise an appropriate exception is raised.

        :param id: A string that is in a valid id format.
        :param ds: Valid dict representing a Nomis dataset.

        :raises TypeError: If the validate_ds() or the validate_id() methods.
        :raises ValueError: Could be raised by the validate_ds() or the validate_id() methods.
        :raises requests.HTTPError: If either connecting to the API is unsuccessful or a negative response is received.

        :return: Unless an exception is raised, will return True indicating the request was successful.
        """
        # Type/value checking
        self.validate_ds(ds, id)
        self.validate_id(id)

        # Make the request: Update/create a dataset.
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            res = self.session.put(
                f'{self.client}/Datasets/{id}',
                data=json.dumps(ds),
                headers=headers,
                verify=False
            )
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            logger.info("Dataset created successfully.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError("Bad input parameter.")
        elif res.status_code == 404:
            logger.info(res.text)
            raise requests.HTTPError(f"Dataset (id: '{id}') already exists.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # GET | PUBLIC
    def get_dataset_dimensions(self, id: str, return_bool: bool = False) -> Union[List[Dimensions], bool]:
        """Method for retrieving dataset dimensions for a dataset with the parameter ID. Makes a GET request to the
        /Datasets/{id}/dimensions endpoint. If successful, then the dimensions are returned by the method, otherwise an
        appropriate exception is raised.

        :param id: A string that is in a valid id format.
        :param return_bool: Return a bool instead of the dimensions themselves

        :raises TypeError: If the validate_id() method detects that the id is not a string.
        :raises ValueError: If the validate_id() method detects that the dataset uuid is not in the correct UUID format.
        :raises requests.HTTPError: If either connecting to the API is unsuccessful or a negative response is received.

        :return: Unless an exception is raised, will return a list of dimensions for the dataset requested.
        """
        # Type/value checking
        self.validate_id(id)

        # Make the request: List dimensions available from a /Datasets/{id}/dimensions.
        try:
            res = self.session.get(
                f'{self.client}/Datasets/{id}/dimensions',
                verify=False
            )
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            # If the request is successful, return the dimensions in the form of an array.
            logger.info("Dataset dimensions retrieved successfully.")
            if return_bool:
                return True
            return res.json()
        elif res.status_code == 400:
            raise requests.HTTPError("Bad input parameters.")
        elif res.status_code == 404:
            if return_bool:
                return False
            raise requests.HTTPError(f"Dataset (id: '{id}') not found, or has no dimensions. ({res.text})")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}. ({res.text}).")

    # PUT | DATASET-ADMIN
    def assign_dimensions_to_dataset(self, id: str, dims: Union[list, dict]) -> bool:
        """Method for assigning dimensions to a dataset which exists in the Nomis database.

        :param id: A string that is in a valid id format.
        :param dims: Object representing the dimensions.

        :raises TypeError: If the validate_id() method detects that the id is not a string.
        :raises ValueError: If the validate_id() method detects that the inputted id is not in the correct UUID format.
        :raises requests.HTTPError: If either connecting to the API is unsuccessful or a negative response is received.

        :return: True if dimensions are assigned successfully, otherwise an exception is raised.
        """
        # Type/value checking
        self.validate_id(id)
        if not isinstance(dims, (list, dict)):
            raise TypeError("Invalid dimensions.")

        # Make request: Assign dimensions to this dataset.
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            res = self.session.put(
                f'{self.client}/Datasets/{id}/dimensions',
                data=json.dumps(dims),
                headers=headers,
                verify=False
            )
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            logger.info("Dimensions assigned successfully.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError(f"Bad input parameters. ({res.text}).")
        elif res.status_code == 403:
            raise requests.HTTPError(f"Forbidden request. ({res.text}).")
        elif res.status_code == 404:
            raise requests.HTTPError(f"Dataset (id: '{id}') not found. ({res.text}).")
        elif res.status_code == 409:
            raise requests.HTTPError(f"Conflicting dimensions. ({res.text}).")
        elif res.status_code == 500:
            raise requests.HTTPError(f"Request unsuccessful due to a server-side error. ({res.text})")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}. ({res.text}).")

    # POST | DATASET-ADMIN
    def append_dataset_observations(self, id: str, obs: Observations) -> bool:
        """Method for appending observations to a dataset in the database.

        :param id: A string that is in a valid id format.
        :param obs: Object representing observation values.

        :raises TypeError: If the validate_id() method detects that the id is not a string, or due to invalid
        observations
        :raises ValueError: If the validate_id() method detects that the inputted id is not in the correct UUID format.
        :raises requests.HTTPError: If either connecting to the API is unsuccessful or a negative response is received.

        :return: Unless an exception is raised, True is returned indicated a successful request.
        """
        # Validation
        self.validate_id(id)
        if not isinstance(obs, (list, dict)):
            raise TypeError(f"Invalid observations.")

        # Make request: Append observation values into this dataset.
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            res = self.session.post(
                f'{self.client}/Datasets/{id}/values',
                data=json.dumps(obs),
                headers=headers,
                verify=False
            )
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            logger.info("Observations appended successfully.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError("Bad input parameters.\n", res.json())
        elif res.status_code == 404:
            raise requests.HTTPError(f"Dataset (id: '{id}') not found.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}. ({res.text})")

    # PUT | DATASET-ADMIN
    def overwrite_dataset_observations(self, id: str, obs_arr: Union[list, dict]) -> bool:
        """Method for overwriting the observations of a dataset in the Nomis database.

        :param id: A string that is in a valid id format.
        :param obs_arr: Array of objects representing data values.

        :raises TypeError: If the validate_id() method detects that the id is not a string, or due to invalid
        observations
        :raises ValueError: If the validate_id() method detects that the inputted id is not
        in the correct UUID format.
        :raises requests.HTTPError: If either connecting to the API is unsuccessful or a negative response is received.

        :return: Unless an exception is raised, True is returned indicated a successful request.
        """
        # Validation
        self.validate_id(id)
        if not isinstance(obs_arr, (list, dict)):
            logger.info("Invalid observations array.")
            return False

        # Make request: Create or update all observation values.
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            res = self.session.put(
                f'{self.client}/Datasets/{id}/values',
                data=json.dumps(obs_arr),
                headers=headers,
                verify=False
            )
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            logger.info("Observations replaced successfully.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError("Bad input parameters.")
        elif res.status_code == 404:
            raise requests.HTTPError(f"Dataset (id: '{id}') not found.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}. ({res.text})")

    # Variables

    # GET | PUBLIC
    def get_variable(self, name: Union[str, None] = None,
                     return_bool: bool = False) -> Union[Variables, List[Variables], bool]:
        """Method for retrieving an existing variable, or simply checking for its existence and returning a Boolean
        confirmation.

        :param name: Unique name of the variable.
        :param return_bool: Admin parameter; returns False instead of raising an exception if variable not found

        :raises TypeError: If the name param is not a string.
        :raises ValueError: If the name param is not in a valid format.
        :raises requests.HTTPError: If either connecting to the API is unsuccessful or a negative response is received.

        :return: Unless an exception is raised, the variable (as a dictionary) is returned.
        """
        # Validation
        if name is not None and not isinstance(name, str):
            raise TypeError("Invalid name, must be a string.")

        # Make request: Lists a specific variable.
        try:
            res = self.session.get(
                f'{self.client}/Variables{f"/{name}" if name is not None else ""}',
                verify=False
            )
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            logger.info(f"Queried variable (name: '{name}') retrieved.")
            return res.json()
        elif res.status_code == 400:
            raise requests.HTTPError(f"Bad input parameters. (Response: {res.text})")
        elif res.status_code == 404:
            if return_bool:
                logger.info(f"Queried variable (name: '{name}') does not exist.")
                return False
            raise requests.HTTPError(f"Queried variable (name: '{name}') not found. (Response: {res.text})")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}. (Response: {res.text})")

    # PUT | VARIABLE-ADMIN
    def create_variable(self, name: str, var: dict) -> bool:
        """Method for creating a new variable.

        :param name: Unique name of the variable.
        :param var: Object representing the variable. Must be a valid dict.

        :raises TypeError: If the name param is not a string, or the var param is not a valid Variable.
        :raises ValueError: If the name param is not in a valid format.
        :raises requests.HTTPError: If either connecting to the API is unsuccessful or a negative response is received.

        :return: Unless an exception is raised, True is returned if the variable does exist, False otherwise.
        """
        # Validation
        if not isinstance(name, str):
            raise TypeError("Invalid name, must be a string.")
        elif not isinstance(var, dict):
            raise TypeError("Invalid variable object.")

        # Make request: Update/create a variable
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            res = self.session.put(
                f'{self.client}/Variables/{name}',
                data=json.dumps(var),
                headers=headers,
                verify=False
            )
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            logger.info(f"Variable (name: '{name}') created successfully.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError("Bad input parameters.")
        elif res.status_code == 404:
            raise requests.HTTPError(f"Variable (name: '{name}') not found.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # GET | PUBLIC
    def get_variable_categories(self, name: str) -> list:
        """Method for retrieving the categories of a variable by name

        :param name: Unique name of the variable.

        :raises TypeError: If the name param is not a string.
        :raises ValueError: If the name param is not in a valid format.
        :raises requests.HTTPError: If either connecting to the API is unsuccessful or a negative response is received.

        :return: A list of categories upon a successful request; an appropriate error will be raised otherwise.
        """
        # Validation
        if not isinstance(name, str):
            raise TypeError("Invalid name, must be a string.")

        # Make request: Lists the categories in a specific variable.
        try:
            res = self.session.get(
                f'{self.client}/Variables/{name}/categories',
                verify=False
            )
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            logger.info(f"Queried variable categories retrieved for variable '{name}'.")
            return res.json()
        elif res.status_code == 400:
            raise requests.HTTPError("Bad input parameters.")
        elif res.status_code == 404:
            raise requests.HTTPError(f"Variable (name: '{name}') not found.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # PUT | VARIABLE-ADMIN
    def create_variable_category(self, name: str, cat_arr: list) -> bool:
        """Method for adding variable categories to a variable in the dataset.

        :param name: Unique name of the variable.
        :param cat_arr: Array of dimension categories.

        :raises TypeError: If the name param is not a string, or the cat_arr param is not a valid list of categories.
        :raises ValueError: If the name param is not in a valid format.
        :raises requests.HTTPError: if either connecting to the API is unsuccessful or a negative response is received.

        :return: True will be returned upon a successful request; an appropriate error will be raised otherwise.
        """
        #  Validation
        if not isinstance(name, str):
            raise TypeError("Invalid name, must be a string.")
        elif not isinstance(cat_arr, list):
            raise TypeError("Invalid category array.")

        # Make request: Add categories to variable.
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            res = self.session.put(
                f'{self.client}/Variables/{name}/categories',
                data=json.dumps(cat_arr),
                headers=headers,
                verify=False
            )
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            logger.info(f"Variable categories created successfully for variable '{name}'.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError("Bad input parameters.")
        elif res.status_code == 404:
            raise requests.HTTPError(f"Variable (name: '{name}') not found.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # POST | VARIABLE-ADMIN
    def update_variable_category(self, name: str, code: str, cat: dict) -> bool:
        """Method for updating a specific variable category

        :param name: Unique name of the variable.
        :param code: Category code
        :param cat: Partial object representing a variable category.

        :raises TypeError: If the name param is not a string, the cat param is not a valid category, or the code is
        invalid.
        :raises ValueError: If the name param is not in a valid format.
        :raises requests.HTTPError: If either connecting to the API is unsuccessful or a negative response is received.

        :return: True will be returned upon a successful request; an appropriate error will be raised otherwise.
        """
        print(cat)
        # Validation
        if not isinstance(name, str):
            logger.info("Invalid name, must be a string.")
            return False
        elif not isinstance(code, str):
            logger.info("Code invalid type.")
            return False
        elif not isinstance(cat, dict):
            logger.info("Invalid category array.")
            return False

        # Make request: Partially update category.
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            res = self.session.patch(
                f'{self.client}/Variables/{name}/categories/{code}',
                headers=headers,
                data=json.dumps(cat),
                verify=False
            )
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            logger.info(f"Variable category updated successfully for variable '{name}'.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError("Bad input parameters.")
        elif res.status_code == 404:
            raise requests.HTTPError(f"Variable (name: '{name}') not found.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")
