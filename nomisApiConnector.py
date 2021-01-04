import requests
import json
from typing import Tuple, Union


# Draft of Nomis API Connector with the basic functionality

class NomisApiConnector:
    def __init__(self, client: str, credentials: Tuple[str, str]) -> None:
        self.client = client
        self.session = requests.Session()   # Begin a session
        self.session.auth = credentials

    def __enter__(self) -> 'NomisApiConnector':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        requests.Session.close(self.session)

    def validate_ds(self, ds: dict) -> bool:
        """
        - Scan through the dictionary elements one by one and:
            - Ensure it exists
            - Ensure the type is correct/valid
        """
        try:
            # Type-checking
            if not isinstance(ds, dict)                                 \
                    or not isinstance(ds["id"], str)                    \
                    or not isinstance(ds["title"], str)                 \
                    or (ds["metadata"] is not None
                        and not isinstance(ds["metadata"], str))        \
                    or (ds["contactId"] is not None
                        and not isinstance(ds["contactId"], str))       \
                    or not isinstance(ds["isAdditive"], bool)           \
                    or not isinstance(ds["isFlagged"], bool)            \
                    or (ds["derivedFrom"] is not None
                        and not isinstance(ds["derivedFrom"], str))     \
                    or not isinstance(ds["restrictedAccess"], bool)     \
                    or not isinstance(ds["online"], bool):
                raise TypeError
            elif not len(ds) != 12: raise KeyError
            print("Success: Dataset Validated")
            return True
        except TypeError: print("Error: Invalid type(s).")
        except KeyError: print("Error: Dataset does not contain sufficient elements.")
        except Exception as e: print(f"Error: {str(e)}")
        return False

    # GET | PUBLIC
    def dataset_exists(self, id: str) -> bool:
        try:
            if not isinstance(id, str):
                print("Error: Invalid id.")
                return False

            # Make the request: Get dataset definition.
            res = self.session.get(f'{self.client}/datasets/{id}')

            # If the dataset exists, the response code will be 200; other responses correspond to the API documentation.
            if res.status_code == 200: print("SUCCESS: Dataset exists.")
            elif res.status_code == 400: print("ERROR: Bad input parameter.")
            elif res.status_code == 404: print("ERROR: Dataset doesn't exist.")
            else: raise

            # .ok will return True if the status code indicates the request was a success, otherwise will return False.
            return res.ok

        # Will except if there is an issue with the request or the response is unexpected.
        except: print("ERROR: Unexpected response or invalid request whilst attempting to clarify a dataset's existence.")
        return False

    # PUT | DATASET-ADMIN - WILL REQUIRE AUTH.
    def create_dataset(self, id: str, ds: dict) -> bool:
        """
        ds: Object representing the dataset.
        """
        try:
            if not isinstance(id, str):
                print("Error: Invalid id.")
                return False
            elif not isinstance(ds, dict):
                print("Error: Invalid dataset.")
                return False
            elif not self.validate_ds(ds):
                print("Error: Dataset contains invalid types/values.")
                return False

            # Make the request: Update/create a dataset.
            res = self.session.put(f'{self.client}/datasets/{id}', data=json.dumps(ds))

            if res.status_code == 200: print("SUCCESS: Dataset uploaded/created successfully.")
            elif res.status_code == 400: print("ERROR: Bad input parameter.")
            elif res.status_code == 404: print("ERROR: Dataset not found.")
            else: raise
            return res.ok

        except: print("ERROR: Unexpected response or invalid request whilst attempting to create a dataset.")
        return False

    # GET | PUBLIC
    def get_dataset_dimensions(self, id: str) -> Union[list, bool]:
        try:
            if not isinstance(id, str):
                print("Error: Invalid id.")
                return False
            # Make the request: List dimensions available from a dataset.
            res = self.session.get(f'{self.client}/datasets/{id}/dimensions')
            if res.status_code == 200:
                # If the request is successful, return the dimensions in the form of an array.
                print("SUCCESS: Dataset dimensions retrieved successfully.")
                return res.json()
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Dataset not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to get dimensions.")
        return False

    # PUT | DATASET-ADMIN
    def assign_dimensions_to_dataset(self, id: str, dims: list) -> bool:
        """
        dims: Object representing the dimensions.
        """
        try:
            if not isinstance(id, str):
                print("Error: Invalid id.")
                return False
            elif not isinstance(dims, list):
                print("Error: Invalid dimensions.")
                return False
            # Make request: Assign dimensions to this dataset.
            res = self.session.put(f'{self.client}/datasets/{id}/dimensions', data=json.dumps(dims))
            if res.status_code == 200: print("SUCCESS: Dimensions assigned successfully.")
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Dataset not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to assign dimensions.")
        return False

    # POST | DATASET-ADMIN
    def append_dataset_observations(self, id: str, obs: list) -> bool:
        """
        obs: Object representing observation values.
        """
        try:
            if not isinstance(id, str):
                print("Error: Invalid id.")
                return False
            elif not isinstance(obs, list):
                print("Error: Invalid observations.")
                return False
            # Make request: Append observation values into this dataset.
            res = self.session.post(f'{self.client}/datasets/{id}/observations', data=json.dumps(obs))
            if res.status_code == 200: print("SUCCESS: Observations appended successfully.")
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Dataset not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to append observations.")
        return False

    # PUT | DATASET-ADMIN
    def overwrite_dataset_observations(self, id: str, obs_arr: list) -> bool:
        """
        obs_arr: Array of objects representing data values.
        """
        try:
            if not isinstance(id, str):
                print("Error: Invalid id.")
                return False
            elif not isinstance(obs_arr, list):
                print("Error: Invalid observations array.")
                return False
            # Make request: Create or update all observation values.
            res = self.session.put(f'{self.client}/datasets/{id}/observations', data=json.dumps(obs_arr))
            if res.status_code == 200: print("SUCCESS: Observations replaced successfully.")
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Dataset not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to overwrite observations.")
        return False

    # GET | PUBLIC
    def variable_exists(self, name: str) -> bool:
        try:
            if not isinstance(name, str):
                print("Error: Invalid name.")
                return False
            # Make request: Lists a specific variable.
            res = self.session.get(f'{self.client}/variables/{name}')
            if res.status_code == 200: print("SUCCESS: Queried variable does exist.")
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Variable not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to overwrite observations.")
        return False

    # PUT | VARIABLE-ADMIN
    def create_variable(self, name: str, var: dict) -> bool:
        """
        name: Must be a valid string, in correct format.
        var: Object representing the variable. Must be a valid array.
        """
        try:
            if not isinstance(name, str):
                print("Error: Invalid name.")
                return False
            elif not isinstance(var, dict):
                print("Error: Invalid variable object.")
                return False
            # Make request: Update/create a variable
            res = self.session.put(f'{self.client}/variables/{name}', json.dumps(var))
            if res.status_code == 200: print("SUCCESS: Variable created successfully.\n", res)
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Variable not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to create a variable.")
        return False

    # GET | PUBLIC
    def get_variable_categories(self, name: str) -> Union[list, bool]:
        try:
            if not isinstance(name, str):
                print("Error: Invalid name.")
                return False
            # Make request: Lists the categories in a specific variable.
            res = self.session.get(f'{self.client}/variables/{name}/categories')
            if res.status_code == 200:
                print("SUCCESS: Queried variable categories retrieved.")
                return res.json()
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Variable not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to get variable categories.")
        return False

    # PUT | VARIABLE-ADMIN
    def create_variable_category(self, name: str, cat_arr: list) -> bool:
        """
        cat_arr: Array of dimension categories.
        """
        try:
            if not isinstance(name, str):
                print("Error: Invalid name.")
                return False
            elif not isinstance(cat_arr, list):
                print("Error: Invalid category array.")
                return False
            if not isinstance(name, str):
                print("Error: Invalid name.")
                return False
            # Make request: Add categories to variable.
            res = self.session.put(f'{self.client}/variables/{name}/categories', data=json.dumps(cat_arr))
            if res.status_code == 200: print("SUCCESS: Variable category created successfully.")
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Variable not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to create variable category.")
        return False

    # POST | VARIABLE-ADMIN
    def update_variable_category(self, name: str, code: str, cat: list) -> bool:
        """
        cat: Partial object representing a variable category.
        """
        try:
            if not isinstance(name, str):
                print("Error: Invalid name.")
                return False
            elif not isinstance(code, str):
                # try: code = str(code)
                # except:
                print("Error: Code invalid type.")
                return False
            elif not isinstance(cat, dict):
                print("Error: Invalid category array.")
                return False
            # Make request: Partially update category.
            res = self.session.patch(f'{self.client}/variables/{name}/categories/{code}', data=json.dumps(cat))
            if res.status_code == 200: print("SUCCESS: Variable category updated successfully.")
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Variable not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to update a variable category.")
        return False

# connector = NomisApiConnector("https://virtserver.swaggerhub.com/SpencerHedger/Nomis-API/2.01", ('user', 'pass'))


