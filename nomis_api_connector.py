from type_hints import *
import requests
import json
from uuid import UUID
# Draft of Nomis API Connector with the basic functionality

# 21/02/2021 changes:
# - dataset_exits() renamed to get_dataset(); new dataset_exists() calls get_dataset() and returns a bool
# - Alterations to the validate_ds() method to acknowledge metadata
# - More informative error messages

# 07/03/2021:
# - Added more detailed doctstrings and updated type hints
# - Added uuid validation

requests.packages.urllib3.disable_warnings() 


class NomisApiConnector:
    """API Connector class for communicating with Nomis' main API. Provides the functionality of appending and altering
    datasets and variables on the Nomis database through the Nomis API.

    :param address: A string of a valid address, either a url or IP address, for connecting to the API
    :type address: str
    :param credentials: Contains the username and password for authentication with the API
    :type credentials: tuple
    :param port: A string or an integer representing the port the API will be served on
    :type port: str|int, optional
    """
    def __init__(self, address: str, credentials: Tuple[str, str], port: Union[str, int, None] = "5001") -> None:
        self.client = f"{str(address)}:{str(port)}" if port is not None else str(address)
        self.session = requests.Session()   # Begin a session
        self.session.auth = credentials

    def __enter__(self) -> 'NomisApiConnector':
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        requests.Session.close(self.session)

    # Datasets

    def validate_ds(self, ds: NomisDataset) -> Union[bool, None]:
        """Method for validating that a dataset is in the correct format and contains the required information. Validation
        is done simply by first ensuring the dataset is the correct type (a Python dict), and then by checking the
        individual keys in the dataset, ensuring they are all in the correct type and format, and if they aren't
        optional that they exist in the first place.

        :param ds: A dictionary representing a dataset ready to be transmitted to the Nomis server.
        :type ds: dict

        :raises TypeError: A TypeError will be raised if the dataset itself or any of its elements are of an incorrect type.
        :raises KeyError: A KeyError will be raised if the dataset is missing elements or has unexpected ones.
        :raises ValueError: A ValueError will be raised in the dataset contains an ID not in a valid UUID format.

        :return: If an exception isn't raised, the method will return True.
        :rtype: bool|None
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

        # This will be reached if and only if no exceptions are raised, indicating a valid dataset
        print(f"SUCCESS: Dataset with {ds['id']} validated.")
        return True

    # Validate id
    def validate_id(self, id: str) -> Union[bool, None]:
        """Method for validating parameter IDs

        :param id: A string that is in a valid ID format.
        :type id: str

        :raises TypeError: A TypeError will be raised if the inputted id is not a string.
        :raises ValueError: A ValueError will be raised if the inputted id is not in the correct format.

        :return: True if the id is valid, otherwise an exception is raised
        :rtype: bool|None
        """
        try:
            if not isinstance(id, str):
                raise TypeError
            # Raise value error if format is incorrect
        except TypeError:
            raise TypeError("ERROR: Invalid id, must be a string.")
        except ValueError:
            raise ValueError("ERROR: ID passed is not in a valid format.")
        except Exception as e:
            raise TypeError(f"Unexpected exception whilst validating parameter types. ({str(e)})")
        return True

    # GET | PUBLIC
    def get_dataset(self, id: str) -> Union[None, NomisDataset]:
        """Method for obtaining a dataset from the Nomis database by its uuid. Makes a GET request to the Nomis API
        at the /Datasets/{id} endpoint, and returns the dataset if the response code is 200; otherwise, an appropriate
        exception is raised.

        :param id: A string that is in a valid ID format.
        :type id: str

        :raises TypeError: A TypeError will be raised if the validate_id() method detects that the id is not a string.
        :raises ValueError: A ValueError will be raised if the validate_id() method detects that the dataset uuid is not in the correct UUID format.
        :raises requests.HTTPError: A HTTPError will be raised if either connecting to the API is unsuccessful or a negative response is received.

        :return: If the request is successful, then return the dataset associated with the inputted ID.
        :rtype: dict|None
        """
        # Type/value checking
        self.validate_id(id)

        # Make the request: Get dataset definition.
        try:
            res = self.session.get(f'{self.client}/Datasets/{id}', verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"ERROR: Unable to connect to client. ({e})")

        # Handle response
        # If the dataset exists, the response code will be 200; other responses correspond to the API documentation.
        if res.status_code == 200:
            print("SUCCESS: Dataset found.")
            return res.json()
        elif res.status_code == 400:
            raise requests.HTTPError("ERROR: Bad input parameter.")
        elif res.status_code == 404:
            raise requests.HTTPError(f"ERROR: Dataset (id: {id}) not found.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # GET | PUBLIC
    def dataset_exists(self, id: str) -> Union[bool, None]:
        """Method for verifying the existence of a dataset in the Nomis database. Makes a GET request to the Nomis API
        at the /Datasets/{id} endpoint, and returns True if the response code is 200, False if the response code is 404
        (i.e., dataset not found), and otherwise raises and appropriate exception.

        :param id: A string that is in a valid ID format.
        :type id: str

        :raises TypeError: A TypeError will be raised if the validate_id() method detects that the id is not a string.
        :raises ValueError: A ValueError will be raised if the validate_id() method detects that the dataset uuid is not in the correct UUID format.
        :raises requests.HTTPError: A HTTPError will be raised if either connecting to the API is unsuccessful or a negative response is received.

        :return: True if dataset exists, else False
        :rtype: bool|None
        """
        # Type/value checking
        self.validate_id(id)

        # Attempt to make the request
        try:
            res = self.session.get(f'{self.client}/Datasets/{id}', verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"ERROR: Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            print(f"Dataset with id {id} found.")
            return True
        elif res.status_code == 404:
            print(f"Dataset with id {id} not found.")
            return False
        elif res.status_code == 400:
            raise requests.HTTPError("ERROR: Bad input parameter.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # PUT | DATASET-ADMIN - WILL REQUIRE AUTH.
    def create_dataset(self, id: str, ds: NomisDataset) -> Union[bool, None]:
        """Method for uploading a dataset to the Nomis database. Makes a PUT request to the /Datasets/{id} endpoint,
        with a valid Dataset object encoded into JSON as the body. True is returned by the method if the dataset
        creation is successful (i.e., a 200 code is received), otherwise an appropriate exception is raised.

        :param id: A string that is in a valid id format.
        :type id: str
        :param ds: Valid dict representing a Nomis dataset.
        :type ds: Dict[str, Union[str, bool, int, None]]

        :raises TypeError: A TypeError could be raised by the validate_ds() or the validate_id() methods.
        :raises ValueError: A ValueError could be raised by the validate_ds() or the validate_id() methods.
        :raises requests.HTTPError: A HTTPError will be raised if either connecting to the API is unsuccessful or a negative response is received.

        :return: Unless an exception is raised, will return True indicating the request was successful.
        :rtype: bool|None
        """
        # Type/value checking
        self.validate_ds(ds)
        self.validate_id(id)
        try:
            if not ds["id"] == id:
                raise ValueError
        except ValueError:
            raise ValueError("Dataset ID does not match parameter ID.")

        # Make the request: Update/create a dataset.
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            res = self.session.put(f'{self.client}/Datasets/{id}', data=json.dumps(ds), headers=headers, verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"ERROR: Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            print("SUCCESS: Dataset created successfully.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError("ERROR: Bad input parameter.")
        elif res.status_code == 404:
            raise requests.HTTPError(f"ERROR: Dataset (id: '{id}') already exists.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # GET | PUBLIC
    def get_dataset_dimensions(self, id: str) -> Union[List[Dimensions], None]:
        """Method for retrieving dataset dimensions for a dataset with the parameter ID. Makes a GET request to the
        /Datasets/{id}/dimensions endpoint. If successful, then the dimensions are returned by the method, otherwise an
        appropriate exception is raised.

        :param id: A string that is in a valid id format.
        :type id: str

        :raises TypeError: A TypeError will be raised if the validate_id() method detects that the id is not a string.
        :raises ValueError: A ValueError will be raised if the validate_id() method detects that the dataset uuid is not in the correct UUID format.
        :raises requests.HTTPError: A HTTPError will be raised if either connecting to the API is unsuccessful or a negative response is received.

        :return: Unless an exception is raised, will return a list of dimensions for the dataset requested.
        :rtype: list|None
        """
        # Type/value checking
        self.validate_id(id)

        # Make the request: List dimensions available from a /Datasets/{id}/dimensions.
        try:
            res = self.session.get(f'{self.client}/Datasets/{id}/dimensions', verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"ERROR: Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            # If the request is successful, return the dimensions in the form of an array.
            print("SUCCESS: Dataset dimensions retrieved successfully.")
            return res.json()
        elif res.status_code == 400:
            raise requests.HTTPError("ERROR: Bad input parameters.")
        elif res.status_code == 404:
            raise requests.HTTPError(f"ERROR: Dataset (id: '{id}') not found, or has no dimensions.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # PUT | DATASET-ADMIN
    def assign_dimensions_to_dataset(self, id: str, dims: Union[list, dict]) -> Union[bool, None]:
        """Method for assigning dimensions to a dataset which exists in the Nomis database.

        :param id: A string that is in a valid id format.
        :type id: str
        :param dims: Object representing the dimensions.
        :type dims: list|dict

        :raises TypeError: A TypeError will be raised if the validate_id() method detects that the id is not a string.
        :raises ValueError: A ValueError will be raised if the validate_id() method detects that the inputted id is not in the correct UUID format.
        :raises requests.HTTPError: A HTTPError will be raised if either connecting to the API is unsuccessful or a negative response is received.

        :return: True if dimensions are assigned successfully, otherwise an exception is raised.
        :rtype: bool|None
        """
        # Type/value checking
        self.validate_id(id)
        if not isinstance(dims, (list, dict)):
            raise TypeError("ERROR: Invalid dimensions.")

        # Make request: Assign dimensions to this dataset.
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            res = self.session.put(f'{self.client}/Datasets/{id}/dimensions',
                                   data=json.dumps(dims), headers=headers, verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"ERROR: Unable to connect to client. ({e})")

        if res.status_code == 200:
            print("SUCCESS: Dimensions assigned successfully.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError("ERROR: Bad input parameters.")
        elif res.status_code == 403:
            raise requests.HTTPError("ERROR: Forbidden request.")
        elif res.status_code == 404:
            raise requests.HTTPError(f"ERROR: Dataset (id: '{id}') not found.")
        elif res.status_code == 409:
            raise requests.HTTPError("ERROR: Conflicting dimensions.")
        elif res.status_code == 500:
            raise requests.HTTPError("ERROR: Request unsuccessful due to a server-side error.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # POST | DATASET-ADMIN
    def append_dataset_observations(self, id: str, obs: Observations) -> bool:
        """Method for appending observations to a dataset in the database.

        :param id: A string that is in a valid id format.
        :type id: str

        :param obs: Object representing observation values.
        :type obs: Dict[str, Union[str, Union[str, Dimensions, Codes]]]

        :raises TypeError: A TypeError will be raised if the validate_id() method detects that the id is not a string, or due to invalid observations
        :raises ValueError: A ValueError will be raised if the validate_id() method detects that the inputted id is not in the correct UUID format.
        :raises requests.HTTPError: A HTTPError will be raised if either connecting to the API is unsuccessful or a negative response is received.

        :return: Unless an exception is raised, True is returned indicated a successful request.
        :rtype: bool|None
        """
        # Validation
        self.validate_id(id)
        if not isinstance(obs, (list, dict)):
            raise TypeError(f"ERROR: Invalid observations.")

        # Make request: Append observation values into this dataset.
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            res = self.session.post(f'{self.client}/Datasets/{id}/values',
                                    data=json.dumps(obs), headers=headers, verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"ERROR: Unable to connect to client. ({e})")
        print(res.status_code)

        # Handle response
        if res.status_code == 200:
            print("SUCCESS: Observations appended successfully.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError("ERROR: Bad input parameters.\n", res.json())
        elif res.status_code == 404:
            raise requests.HTTPError(f"ERROR: Dataset (id: '{id}') not found.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # PUT | DATASET-ADMIN
    def overwrite_dataset_observations(self, id: str, obs_arr: list) -> bool:
        """Method for overwriting the observations of a dataset in the Nomis database.

        :param id: A string that is in a valid id format.
        :type id: str

        :param obs_arr: Array of objects representing data values.
        :type obs_arr: List[Observations]

        :raises TypeError: A TypeError will be raised if the validate_id() method detects that the id is not a string, or due to invalid observations
        :raises ValueError: A ValueError will be raised if the validate_id() method detects that the inputted id is not in the correct UUID format.
        :raises requests.HTTPError: A HTTPError will be raised if either connecting to the API is unsuccessful or a negative response is received.

        :return: Unless an exception is raised, True is returned indicated a successful request.
        :rtype: bool|None
        """
        # Validation
        self.validate_id(id)
        if not isinstance(obs_arr, (list, dict)):
            print("ERROR: Invalid observations array.")
            return False

        # Make request: Create or update all observation values.
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            res = self.session.put(f'{self.client}/Datasets/{id}/values',
                                   data=json.dumps(obs_arr), headers=headers, verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"ERROR: Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            print("SUCCESS: Observations replaced successfully.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError("ERROR: Bad input parameters.")
        elif res.status_code == 404:
            raise requests.HTTPError(f"ERROR: Dataset (id: '{id}') not found.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # Variables

    # GET | PUBLIC
    def variable_exists(self, name: str) -> Union[bool, None]:
        """Method for checking the existence of a variable by name.

        :param name: Unique name of the variable.
        :type name: str

        :raises TypeError: A TypeError will be raised if the name param is not a string.
        :raises ValueError: A ValueError will be raised if the name param is not in a valid format.
        :raises requests.HTTPError: A HTTPError will be raised if either connecting to the API is unsuccessful or a negative response is received.

        :return: Unless an exception is raised, True is returned if the variable does exist, False otherwise.
        :rtype: bool|None
        """
        # Validation
        if not isinstance(name, str):
            raise TypeError("ERROR: Invalid name, must be a string.")

        # Make request: Lists a specific variable.
        try:
            res = self.session.get(f'{self.client}/Variables/{name}', verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"ERROR: Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            print(f"Queried variable (name: '{name}') does exist.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError("ERROR: Bad input parameters.")
        elif res.status_code == 404:
            print(f"Variable (name: '{name}') not found.")
            return False
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # PUT | VARIABLE-ADMIN
    def create_variable(self, name: str, var: dict) -> Union[bool, None]:
        """Method for creating a new variable.

        :param name: Unique name of the variable.
        :type name: str
        :param var: Object representing the variable. Must be a valid dict.
        :type var: dict

        :raises TypeError: A TypeError will be raised if the name param is not a string, or the var param is not a valid Variable.
        :raises ValueError: A ValueError will be raised if the name param is not in a valid format.
        :raises requests.HTTPError: A HTTPError will be raised if either connecting to the API is unsuccessful or a negative response is received.

        :return: Unless an exception is raised, True is returned if the variable does exist, False otherwise.
        :rtype: bool|None
        """
        # Validation
        if not isinstance(name, str):
            raise TypeError("ERROR: Invalid name, must be a string.")
        elif not isinstance(var, dict):
            raise TypeError("ERROR: Invalid variable object.")

        # Make request: Update/create a variable
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            res = self.session.put(f'{self.client}/Variables/{name}', json.dumps(var), headers=headers, verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"ERROR: Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            print(f"SUCCESS: Variable (name: '{name}') created successfully.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError("ERROR: Bad input parameters.")
        elif res.status_code == 404:
            raise requests.HTTPError(f"ERROR: Variable (name: '{name}') not found.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # GET | PUBLIC
    def get_variable_categories(self, name: str) -> Union[list, None]:
        """Method for retrieving the categories of a variable by name

        :param name: Unique name of the variable.
        :type name: str

        :raises TypeError: A TypeError will be raised if the name param is not a string.
        :raises ValueError: A ValueError will be raised if the name param is not in a valid format.
        :raises requests.HTTPError: A HTTPError will be raised if either connecting to the API is unsuccessful or a negative response is received.

        :return: A list of categories upon a successful request; an appropriate error will be raised otherwise.
        :rtype: list|None
        """
        # Validation
        if not isinstance(name, str):
            raise TypeError("ERROR: Invalid name, must be a string.")

        # Make request: Lists the categories in a specific variable.
        try:
            res = self.session.get(f'{self.client}/Variables/{name}/categories')
        except Exception as e:
            raise requests.ConnectionError(f"ERROR: Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            print(f"SUCCESS: Queried variable categories retrieved for variable '{name}'.")
            return res.json()
        elif res.status_code == 400:
            raise requests.HTTPError("ERROR: Bad input parameters.")
        elif res.status_code == 404:
            raise requests.HTTPError(f"ERROR: Variable (name: '{name}') not found.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # PUT | VARIABLE-ADMIN
    def create_variable_category(self, name: str, cat_arr: list) -> Union[bool, None]:
        """Method for adding variable categories to a variable in the dataset.

        :param name: Unique name of the variable.
        :type name: str
        :param cat_arr: Array of dimension categories.
        :type cat_arr: list

        :raises TypeError: A TypeError will be raised if the name param is not a string, or the cat_arr param is not a valid list of categories.
        :raises ValueError: A ValueError will be raised if the name param is not in a valid format.
        :raises requests.HTTPError: A HTTPError will be raised if either connecting to the API is unsuccessful or a negative response is received.

        :return: True will be returned upon a successful request; an appropriate error will be raised otherwise.
        :rtype: True|None
        """
        #  Validation
        if not isinstance(name, str):
            raise TypeError("ERROR: Invalid name, must be a string.")
        elif not isinstance(cat_arr, list):
            raise TypeError("ERROR: Invalid category array.")

        # Make request: Add categories to variable.
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            res = self.session.put(f'{self.client}/Variables/{name}/categories',
                                   data=json.dumps(cat_arr), headers=headers, verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"ERROR: Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            print(f"SUCCESS: Variable categories created successfully for variable '{name}'.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError("ERROR: Bad input parameters.")
        elif res.status_code == 404:
            raise requests.HTTPError(f"ERROR: Variable (name: '{name}') not found.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")

    # POST | VARIABLE-ADMIN
    def update_variable_category(self, name: str, code: str, cat: dict) -> bool:
        """Method for updating a specific variable category

        :param name: Unique name of the variable.
        :type name: str
        :param code: Category code
        :type code: str
        :param cat: Partial object representing a variable category.
        :type cat: dict

        :raises TypeError: A TypeError will be raised if the name param is not a string, the cat param is not a valid category, or the code is invalid.
        :raises ValueError: A ValueError will be raised if the name param is not in a valid format.
        :raises requests.HTTPError: A HTTPError will be raised if either connecting to the API is unsuccessful or a negative response is received.

        :return: True will be returned upon a successful request; an appropriate error will be raised otherwise.
        :rtype: True|None
        """
        # Validation
        if not isinstance(name, str):
            print("ERROR: Invalid name, must be a string.")
            return False
        elif not isinstance(code, str):
            print("ERROR: Code invalid type.")
            return False
        elif not isinstance(cat, dict):
            print("ERROR: Invalid category array.")
            return False

        # Make request: Partially update category.
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            res = self.session.patch(f'{self.client}/Variables/{name}/categories/{code}',
                                     headers=headers, data=json.dumps(cat), verify=False)
        except Exception as e:
            raise requests.ConnectionError(f"ERROR: Unable to connect to client. ({e})")

        # Handle response
        if res.status_code == 200:
            print(f"SUCCESS: Variable category updated successfully for variable '{name}'.")
            return True
        elif res.status_code == 400:
            raise requests.HTTPError("ERROR: Bad input parameters.")
        elif res.status_code == 404:
            raise requests.HTTPError(f"ERROR: Variable (name: '{name}') not found.")
        else:
            raise Exception(f"Unexpected response with status code {res.status_code}.")




