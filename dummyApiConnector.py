import requests
import json
from typing import Union, Tuple

#todo:

class DummyApiConnector:
    def __init__(self, client: str, credentials: Tuple[str, str]) -> None:
        self.client = str(client)
        self.session = requests.Session()  # Begin a session
        self.session.auth = credentials
        self._contextManaged: bool = False

    def __enter__(self) -> 'DummyApiConnector':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        requests.Session.close(self.session)

    def validate_parameters(self, client, credentials):
        pass

    def validate_ds(self, ds: dict) -> bool:
        """
        - Scan through the dictionary elements one by one and:
            - Ensure it exists
            - Ensure its type is valid
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
        """
        id: Must be a valid string, in correct format.
        """
        try:
            if not isinstance(id, str):
                print("Error: Invalid id.")
                return False

            # Make the request: Get dataset definition.
            res = self.session.get(f'{self.client}/datasets/{id}')

            print('{}\n{}\n{}\nBody: {}'.format(
                '-----------DATASET_EXISTS-----------',
                res.request.method + ' ' + res.request.url,
                '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
                res.request.body
            ))

            # Print the request being made and the endpoint:
            print("\nResponse: ")
            # If the dataset exists, the response code will be 200; other responses correspond to the API documentation.
            if res.status_code == 200: print("SUCCESS: Dataset exists.\n", res)
            elif res.status_code == 400: print("ERROR: Bad input parameter.")
            elif res.status_code == 404: print("ERROR: Dataset doesn't exist.")
            else: raise

            # .ok will return True if the status code indicates the request was a success, otherwise will return False.
            return res.ok

        # Will except if there is an issue with the request or the response is unexpected.
        except: print("ERROR: Unexpected response or invalid request whilst attempting to clarify the existence of a dataset.")
        return False

    # PUT | DATASET-ADMIN - WILL REQUIRE AUTH.
    def create_dataset(self, id: str, ds: dict) -> bool:
        """
        id: Must be a valid string, in correct format.
        ds: Object representing the dataset. The ds object will have a validtion method, so will call ds.validate.
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

            print('{}\n{}\n{}\nBody: \n{}'.format(
                '-----------CREATE_DATASET-----------',
                res.request.method + ' ' + res.request.url,
                '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
                json.dumps(ds, indent=2)
            ))

            print("\nResponse: ")
            if res.status_code == 200: print("SUCCESS: Dataset uploaded/created successfully.\n", res)
            elif res.status_code == 400: print("ERROR: Bad input parameter.")
            elif res.status_code == 404: print("ERROR: Dataset not found.")
            else: raise
            return res.ok

        except: print("ERROR: Unexpected response or invalid request whilst attempting to create a dataset.")
        return False

    # GET | PUBLIC
    def get_dataset_dimensions(self, id: str) -> Union[str, list, bool]:
        """
        id: Must be a valid string, in correct format.
        """
        try:
            if not isinstance(id, str):
                print("Error: Invalid id.")
                return False

            # Make the request: List dimensions available from a dataset.
            res = self.session.get(f'{self.client}/datasets/{id}/dimensions')

            print('{}\n{}\n{}\nBody: {}'.format(
                '-----------GET_DATASET_DIMENSIONS-----------',
                res.request.method + ' ' + res.request.url,
                '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
                res.request.body,
            ))

            print("Response: ")
            if res.status_code == 200:
                # If the request is successful, return the dimensions in the form of an array.
                print("SUCCESS: Dataset dimensions retrieved successfully.\n", res)
                return json.dumps(json.loads(res.text), indent=2)
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Dataset not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to get dimensions.")
        return False

    # PUT | DATASET-ADMIN
    def assign_dimensions_to_dataset(self, id: str, dims: list) -> bool:
        """
        id: Must be a valid string, in correct format.
        dims: Object representing the dimensions. Must be a valid array.
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

            print('{}\n{}\n{}\nBody: {}'.format(
                '-----------ASSIGN_DIMENSIONS_TO_DATASET-----------',
                res.request.method + ' ' + res.request.url,
                '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
                '\n' + json.dumps(dims, indent=2),
            ))

            print("Response: ")
            if res.status_code == 200: print("SUCCESS: Dimensions assigned successfully.\n", res)
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Dataset not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to assign dimensions.")
        return False

    # POST | DATASET-ADMIN
    def append_dataset_observations(self, id: str, obs: list) -> bool:
        """
        id: Must be a valid string, in correct format.
        obs: Object representing observation values. Must be a valid array.
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

            print('{}\n{}\n{}\nBody: {}'.format(
                '-----------APPEND_DATASET_OBSERVATIONS-----------',
                res.request.method + ' ' + res.request.url,
                '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
                '\n' + json.dumps(obs, indent=2),
            ))

            print("Response: ")
            if res.status_code == 200: print("SUCCESS: Observations appended successfully.\n", res)
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Dataset not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to append observations.")
        return False

    # PUT | DATASET-ADMIN
    def overwrite_dataset_observations(self, id: str, obs_arr: list) -> bool:
        """
        id: Must be a valid string, in correct format.
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

            print('{}\n{}\n{}\nBody: {}\n'.format(
                '-----------OVERWRITE_DATASET_OBSERVATIONS-----------',
                res.request.method + ' ' + res.request.url,
                '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
                '\n' + json.dumps(obs_arr, indent=2),
            ))

            print("Response: ")
            if res.status_code == 200: print("SUCCESS: Observations replaced successfully.\n", res)
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Dataset not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to overwrite observations.")
        return False

    # GET | PUBLIC
    def variable_exists(self, name: str) -> bool:
        """
        name: Must be a valid string, in correct format.
        """
        try:
            if not isinstance(name, str):
                print("Error: Invalid name.")
                return False
            # Make request: Lists a specific variable.
            res = self.session.get(f'{self.client}/variables/{name}')   # changed from put to get oops

            print('{}\n{}\n{}\nBody: {}\n'.format(
                '-----------VARIABLE_EXISTS-----------',
                res.request.method + ' ' + res.request.url,
                '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
                res.request.body,
            ))

            print("Response: ")
            if res.status_code == 200: print("SUCCESS: Queried variable does exist.\n", res)
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
        var: Object representing the variable. Must be a valid dict object.
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

            print('{}\n{}\n{}\nBody: \n{}\n'.format(
                '-----------CREATE_VARIABLE-----------',
                res.request.method + ' ' + res.request.url,
                '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
                json.dumps(var, indent=2),
            ))

            print("Response: ")
            if res.status_code == 200: print("SUCCESS: Variable created successfully.\n", res)
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Variable not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to create a variable.")
        return False

    # GET | PUBLIC
    def get_variable_categories(self, name: str) -> Union[str, list, bool]:
        """
        name: Must be a valid string, in correct format.
        """
        try:
            if not isinstance(name, str):
                print("Error: Invalid name.")
                return False
            # Make request: Lists the categories in a specific variable.
            res = self.session.get(f'{self.client}/variables/{name}/categories')

            print('{}\n{}\n{}\nBody: {}\n'.format(
                '-----------GET_VARIABLE_CATEGORIES-----------',
                res.request.method + ' ' + res.request.url,
                '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
                res.request.body,
            ))

            print("Response: ")
            if res.status_code == 200:
                # If successful, return the variable categories in the form of an array
                print("SUCCESS: Queried variable categories retrieved.\n", res)
                return json.dumps(json.loads(res.text), indent=2)
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Variable not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to get variable categories.")
        return False

    # PUT | VARIABLE-ADMIN
    def create_variable_category(self, name: str, cat_arr: list) -> bool:
        """
        name: Must be a valid string, in correct format.
        cat_arr: Array of variable categories. Must be a valid array.
        """
        try:
            if not isinstance(name, str):
                print("Error: Invalid name.")
                return False
            elif not isinstance(cat_arr, list):
                print("Error: Invalid category array.")
                return False
            # Make request: Add categories to variable.
            res = self.session.put(f'{self.client}/variables/{name}/categories', data=json.dumps(cat_arr))

            print('{}\n{}\n{}\nBody: {}\n'.format(
                '-----------CREATE_VARIABLE_CATEGORY-----------',
                res.request.method + ' ' + res.request.url,
                '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
                '\n' +json.dumps(cat_arr, indent=2),
            ))

            print("Response: ")
            if res.status_code == 200: print("SUCCESS: Variable category created successfully.\n", res)
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Variable not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to create variable category.")
        return False

    # POST | VARIABLE-ADMIN
    def update_variable_category(self, name: str, code: str, cat: list) -> bool:
        """
        name: Must be a valid string, correctly formatted.
        code: Must be a valid string, correctly formatted.
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

            print('{}\n{}\n{}\n\nBody: {}\n'.format(
                '-----------UPDATE_VARIABLE_CATEGORY-----------',
                res.request.method + ' ' + res.request.url,
                '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
                '\n' + json.dumps(cat, indent=2),
            ))

            print("Response: ")
            if res.status_code == 200: print("SUCCESS: Variable category updated successfully.\n", res)
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Variable not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to update a variable category.")
        return False


# c = ConfigManager()
# conf = c.decode_into_configuration()
# nomis_creds = c.decode_into_nomis_credentials()
# nomis_conn = c.decode_into_nomis_connection_info()
# nomis = c.create_api_connection_info(nomis_creds, nomis_conn)
# credentials = nomis.get_credentials()
# client = nomis.get_client()

# creds = ('user', 'pass')
# addr = f"https://virtserver.swaggerhub.com/SpencerHedger/Nomis-API/2.01"
# cat = obs = dims = [1,2,3,4,5]
# obs_arr = [obs,obs,obs]
# cat_arr = [cat,cat,cat]

# connector = DummyApiConnector(addr, creds)
#
# with open("./dummyDataset.json") as f:
#     dummy_dataset = json.loads(f.read())
#
# with DummyApiConnector(addr, creds) as connector:
#     print("")
#     connector.dataset_exists('1')
#     print("")
#     connector.create_dataset('1', dummy_dataset)
#     print("")
#     print(connector.get_dataset_dimensions('1'))
#     print("")
#     connector.assign_dimensions_to_dataset('1', dims)
#     print("")
#     connector.append_dataset_observations('1', obs)
#     print("")
#     connector.overwrite_dataset_observations('1', obs_arr)
#     print("")
#     connector.variable_exists('1')
#     print("")
#     print(connector.get_variable_categories('1'))
#     print("")
#     connector.create_variable_category('1',cat_arr)
#     print("")
#     connector.update_variable_category('1','1',cat)

