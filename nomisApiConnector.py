from typing import Union, Tuple, Dict, Any
import requests
import json
# Draft of Nomis API Connector with the basic functionality

# 21/02/2021 changes:
# - dataset_exits() renamed to get_dataset(); new dataset_exists() calls get_dataset() and returns a bool
# - Alterations to the validate_ds() method to acknowledge metadata
# - More informative error messages


requests.packages.urllib3.disable_warnings() 


class NomisApiConnector:
    def __init__(self, address: str, credentials: Tuple[str, str], port: Union[str, None] = "5001") -> None:
        self.client = f"{str(address)}:{str(port)}" if port is not None else str(address)
        self.session = requests.Session()   # Begin a session
        self.session.auth = credentials

    def __enter__(self) -> 'NomisApiConnector':
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        requests.Session.close(self.session)

    # Datasets

    def validate_ds(self, ds: dict) -> bool:
        """
        - Scan through the dictionary elements one by one and:
            - Ensure it exists
            - Ensure the type is correct/valid
        """
        try:
            # Type-checking: todo: also check for valid uuid
            if not isinstance(ds, dict)                                 \
                    or not isinstance(ds["id"], str)                    \
                    or not isinstance(ds["title"], str)                 \
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
            print(f"SUCCESS: Dataset with {ds['id']} validated.")
            return True
        except TypeError: print("ERROR: Invalid type(s).")
        except KeyError: print("ERROR: Dataset does not contain sufficient elements.")
        except Exception as e: print(f"ERROR: {str(e)}")
        return False

    # GET | PUBLIC
    def get_dataset(self, id: str) -> Union[bool, Dict[str, str]]:
        try:
            if not isinstance(id, str):
                print("ERROR: Invalid id, must be a string.")
                return False

            # Make the request: Get dataset definition.
            res = self.session.get(f'{self.client}/Datasets/{id}', verify=False)
            # If the dataset exists, the response code will be 200; other responses correspond to the API documentation.

            if res.status_code == 200:
                print("SUCCESS: Dataset found.")
                return res.json()
            elif res.status_code == 400: print("ERROR: Bad input parameter.")
            elif res.status_code == 404: print(f"ERROR: Dataset (id: {id}) not found.")
            else: raise Exception("Unexpected response.")

            # .ok will return True if the status code indicates the request was a success, otherwise will return False.
            return res.ok

        # Will except if there is an issue with the request or the response is unexpected.
        except Exception as e:
            # print(res)
            print(f"ERROR: Unexpected response or invalid request whilst attempting to clarify a dataset's existence. "
                  f"({str(e)}")
        return False

    # GET | PUBLIC
    def dataset_exists(self, id: str) -> bool:
        try:
            res = self.get_dataset(id)
            return False if res is False else True
        except Exception as e:
            print(f"ERROR: Unexpected response or invalid request whilst attempting to clarify a dataset's existence. "
                  f"({str(e)}")
        return False

    # PUT | DATASET-ADMIN - WILL REQUIRE AUTH.
    def create_dataset(self, id: str, ds: dict) -> bool:
        """
        ds: Object representing the dataset.
        """
        try:
            if not isinstance(id, str):
                print("ERROR: Invalid id, must be a string.")
                return False
            elif not isinstance(ds, dict):
                print("ERROR: Invalid dataset.")
                return False
            elif not self.validate_ds(ds):
                print("ERROR: Dataset contains invalid types/values.")
                return False

            # Make the request: Update/create a dataset.
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            res = self.session.put(f'{self.client}/Datasets/{id}', data=json.dumps(ds), headers=headers, verify=False)

            if res.status_code == 200: print("SUCCESS: Dataset created successfully.")
            elif res.status_code == 400: print("ERROR: Bad input parameter.")
            elif res.status_code == 404: print(f"ERROR: Dataset (id: '{id}') already exists.")
            else: raise Exception("Unexpected response.")
            return res.ok
        except Exception as e:
            print(f"ERROR: Unexpected response or invalid request whilst attempting to create a dataset. ({str(e)})")
        return False

    # GET | PUBLIC
    def get_dataset_dimensions(self, id: str) -> Union[list, bool]:
        try:
            if not isinstance(id, str):
                print("ERROR: Invalid id, must be a string.")
                return False
            # Make the request: List dimensions available from a dataset.
            res = self.session.get(f'{self.client}/Datasets/{id}/dimensions', verify=False)
            if res.status_code == 200:
                # If the request is successful, return the dimensions in the form of an array.
                print("SUCCESS: Dataset dimensions retrieved successfully.")
                return res.json()
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print(f"ERROR: Dataset (id: '{id}') not found, or has no dimensions.")
            else: raise Exception("Unexpected response.")
            return res.ok
        except Exception as e:
            print(f"ERROR: Unexpected response or invalid request whilst attempting to get dimensions. ({str(e)})")
        return False

    # PUT | DATASET-ADMIN
    def assign_dimensions_to_dataset(self, id: str, dims: Union[list, dict]) -> bool:
        """
        dims: Object representing the dimensions.
        """
        try:
            if not isinstance(id, str):
                print("ERROR: Invalid id, must be a string.")
                return False
            elif not isinstance(dims, (list, dict)):
                print("ERROR: Invalid dimensions.")
                return False

            # Make request: Assign dimensions to this dataset.
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            res = self.session.put(f'{self.client}/Datasets/{id}/dimensions',
                                   data=json.dumps(dims), headers=headers, verify=False)
            if res.status_code == 200: print("SUCCESS: Dimensions assigned successfully.")
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 403: print("ERROR: Forbidden request.")
            elif res.status_code == 404: print(f"ERROR: Dataset (id: '{id}') not found.")
            elif res.status_code == 409: print("ERROR: Conflicting dimensions.")
            elif res.status_code == 500: print("ERROR: Request unsuccessful due to a server-side error.")
            else: raise Exception(f"Unexpected response, status code = {str(res.status_code)}.")
            return res.ok
        except Exception as e:
            print(f"ERROR: Unexpected response or invalid request whilst attempting to assign dimensions ({str(e)})")
        return False

    # POST | DATASET-ADMIN
    def append_dataset_observations(self, id: str, obs: list) -> bool:
        """
        obs: Object representing observation values.
        """
        try:
            if not isinstance(id, str):
                print("ERROR: Invalid id, must be a string.")
                return False
            elif not isinstance(obs, (list, dict)):
                print(f"ERROR: Invalid observations.")
                return False
            # Make request: Append observation values into this dataset.
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            res = self.session.post(f'{self.client}/Datasets/{id}/values',
                                    data=json.dumps(obs), headers=headers, verify=False)
            if res.status_code == 200: print("SUCCESS: Observations appended successfully.")
            elif res.status_code == 400: print("ERROR: Bad input parameters.\n", res.json())
            elif res.status_code == 404: print(f"ERROR: Dataset (id: '{id}') not found.")
            else:
                print(res.json())
                raise Exception("Unexpected response.")
            return res.ok
        except Exception as e:
            print(f"ERROR: Unexpected response or invalid request whilst attempting to append observations. ({str(e)})")
        return False

    # PUT | DATASET-ADMIN
    def overwrite_dataset_observations(self, id: str, obs_arr: list) -> bool:
        """
        obs_arr: Array of objects representing data values.
        """
        try:
            if not isinstance(id, str):
                print("ERROR: Invalid id, must be a string.")
                return False
            elif not isinstance(obs_arr, (list, dict)):
                print("ERROR: Invalid observations array.")
                return False
            # Make request: Create or update all observation values.
            headers={'Content-type': 'application/json', 'Accept': 'application/json'}
            res = self.session.put(f'{self.client}/Datasets/{id}/values',
                                   data=json.dumps(obs_arr), headers=headers, verify=False)
            if res.status_code == 200: print("SUCCESS: Observations replaced successfully.")
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print(f"ERROR: Dataset (id: '{id}') not found.")
            else: raise Exception("Unexpected response.")
            return res.ok
        except Exception as e:
            print(f"ERROR: Unexpected response or invalid request whilst attempting to overwrite observations. "
                  f"({str(e)})")
        return False

    # Variables

    # GET | PUBLIC
    def variable_exists(self, name: str) -> bool:
        try:
            if not isinstance(name, str):
                print("ERROR: Invalid name, must be a string.")
                return False
            # Make request: Lists a specific variable.
            res = self.session.get(f'{self.client}/Variables/{name}', verify=False)
            if res.status_code == 200: print(f"Queried variable (name: '{name}') does exist.")
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print(f"Variable (name: '{name}') not found.")
            else: raise Exception("Unexpected response.")
            return res.ok
        except Exception as e:
            print(f"ERROR: Unexpected response or invalid request whilst attempting to clarify a variable's existence. "
                  f"({str(e)})")
        return False

    # PUT | VARIABLE-ADMIN
    def create_variable(self, name: str, var: dict) -> bool:
        """
        name: Must be a valid string, in correct format.
        var: Object representing the variable. Must be a valid array.
        """
        try:
            if not isinstance(name, str):
                print("ERROR: Invalid name, must be a string.")
                return False
            elif not isinstance(var, dict):
                print("ERROR: Invalid variable object.")
                return False

            # Make request: Update/create a variable
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            res = self.session.put(f'{self.client}/Variables/{name}', json.dumps(var), headers=headers, verify=False)
            if res.status_code == 200: print(f"SUCCESS: Variable (name: '{name}') created successfully.")
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print(f"ERROR: Variable (name: '{name}') not found.")
            else: raise Exception("Unexpected response.")
            return res.ok
        except Exception as e:
            print(f"ERROR: Unexpected response or invalid request whilst attempting to create a variable. ({str(e)})")
        return False

    # GET | PUBLIC
    def get_variable_categories(self, name: str) -> Union[list, bool]:
        try:
            if not isinstance(name, str):
                print("ERROR: Invalid name, must be a string.")
                return False
            # Make request: Lists the categories in a specific variable.
            res = self.session.get(f'{self.client}/Variables/{name}/categories')
            if res.status_code == 200: print(f"SUCCESS: Queried variable categories retrieved for variable '{name}'.")
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print(f"ERROR: Variable (name: '{name}') not found.")
            else: raise Exception("Unexpected response.")
            return res.ok
        except Exception as e:
            print(f"ERROR: Unexpected response or invalid request whilst attempting to get variable categories. "
                  f"({str(e)})")
        return False

    # PUT | VARIABLE-ADMIN
    def create_variable_category(self, name: str, cat_arr: list) -> bool:
        """
        cat_arr: Array of dimension categories.
        """
        try:
            if not isinstance(name, str):
                print("ERROR: Invalid name, must be a string.")
                return False
            elif not isinstance(cat_arr, list):
                print("ERROR: Invalid category array.")
                return False
            if not isinstance(name, str):
                print("ERROR: Invalid name.")
                return False
            # Make request: Add categories to variable.
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            res = self.session.put(f'{self.client}/Variables/{name}/categories',
                                   data=json.dumps(cat_arr), headers=headers, verify=False)
            if res.status_code == 200: print(f"SUCCESS: Variable categories created successfully for variable '{name}'.")
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print(f"ERROR: Variable (name: '{name}') not found.")
            else: raise Exception("Unexpected response.")
            return res.ok
        except Exception as e:
            print(f"ERROR: Unexpected response or invalid request whilst attempting to create variable category. "
                  f"({str(e)})")
        return False

    # POST | VARIABLE-ADMIN
    def update_variable_category(self, name: str, code: str, cat: dict) -> bool:
        """
        cat: Partial object representing a variable category.
        """
        try:
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
            res = self.session.patch(f'{self.client}/Variables/{name}/categories/{code}', data=json.dumps(cat))
            if res.status_code == 200: print(f"SUCCESS: Variable category updated successfully for variable '{name}'.")
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print(f"ERROR: Variable (name: '{name}') not found.")
            else:
                print(res.json())
                raise Exception("Unexpected response.")
            return res.ok
        except Exception as e:
            print(f"ERROR: Unexpected response or invalid request whilst attempting to update a variable category. "
                  f"({str(e)})")
        return False



