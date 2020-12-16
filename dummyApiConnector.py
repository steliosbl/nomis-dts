import requests
import json
from typing import *
# from configManager import ConfigManager

#todo:


class DummyApiConnector:
    def __init__(self, client: str, credentials: Tuple[str, str]) -> None:
        self.client = client
        # Begin a session
        self.session = requests.Session()
        self.session.auth = credentials

    # GET | PUBLIC
    def dataset_exists(self, id: str) -> bool:
        try:
            # Make the request: Get dataset definition.
            res = self.session.get(f'{self.client}/datasets/{id}')

            # Print the request being made and the endpoint:
            print('GET, /datasets/{id}')

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
    def create_dataset(self, id: str, ds: str) -> bool:
        """
        ds: Object representing the dataset.
        """
        try:
            # Make the request: Update/create a dataset.
            res = self.session.put(f'{self.client}/datasets/{id}', data=json.dumps(ds))

            print("PUT, /datasets/{id}")

            if res.status_code == 200: print("SUCCESS: Dataset uploaded/created successfully.\n", res)
            elif res.status_code == 400: print("ERROR: Bad input parameter.")
            elif res.status_code == 404: print("ERROR: Dataset not found.")
            else: raise
            return res.ok

        except: print("ERROR: Unexpected response or invalid request whilst attempting to create a dataset.")
        return False

    # GET | PUBLIC
    def get_dataset_dimensions(self, id: str) -> Union[list, bool]:
        try:
            # Make the request: List dimensions available from a dataset.
            res = self.session.get(f'{self.client}/datasets/{id}/dimensions')

            print("GET, /datasets/{id}/dimensions")

            if res.status_code == 200:
                # If the request is successful, return the dimensions in the form of an array.
                print("SUCCESS: Dataset dimensions retrieved successfully.\n", res)
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
            # Make request: Assign dimensions to this dataset.
            res = self.session.put(f'{self.client}/datasets/{id}/dimensions', data=json.dumps(dims))

            print("PUT, /datasets/{id}/dimensions")

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
        obs: Object representing observation values.
        """
        try:
            # Make request: Append observation values into this dataset.
            res = self.session.post(f'{self.client}/datasets/{id}/observations', data=json.dumps(obs))

            print("POST, /datasets/{id}/observations")

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
        obs_arr: Array of objects representing data values.
        """
        try:
            # Make request: Create or update all observation values.
            res = self.session.put(f'{self.client}/datasets/{id}/observations', data=json.dumps(obs_arr))

            print("PUT, /datasets/{id}/observations")

            if res.status_code == 200: print("SUCCESS: Observations replaced successfully.\n", res)
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Dataset not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to overwrite observations.")
        return False

    # GET | PUBLIC
    def variable_exists(self, name: str) -> bool:
        try:
            # Make request: Lists a specific variable.
            res = self.session.put(f'{self.client}/variables/{name}')

            print("GET, /variables/{name}")

            if res.status_code == 200: print("SUCCESS: Queried variable does exist.\n", res)
            elif res.status_code == 400: print("ERROR: Bad input parameters.")
            elif res.status_code == 404: print("ERROR: Variable not found.")
            else: raise
            return res.ok
        except: print("ERROR: Unexpected response or invalid request whilst attempting to overwrite observations.")
        return False

    # GET | PUBLIC
    def get_variable_categories(self, name: str) -> Union[list, bool]:
        try:
            # Make request: Lists the categories in a specific variable.
            res = self.session.get(f'{self.client}/variables/{name}/categories')

            print("GET, /variables/{name}/categories")

            if res.status_code == 200:
                # If successful, return the variable categories in the form of an array
                print("SUCCESS: Queried variable categories retrieved.\n", res)
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
            # Make request: Add categories to variable.
            res = self.session.put(f'{self.client}/variables/{name}/categories', data=json.dumps(cat_arr))

            print("PUT, /variables/{name}/categories")

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
        cat: Partial object representing a variable category.
        """
        try:
            # Make request: Partially update category.
            res = self.session.patch(f'{self.client}/variables/{name}/categories/{code}', data=json.dumps(cat))

            print("POST, /variables/{name}/categories/{code}")

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

creds = ('user', 'pass')
addr = f"https://virtserver.swaggerhub.com/SpencerHedger/Nomis-API/2.01"
cat = obs = dims = [1,2,3,4,5]
obs_arr = [obs,obs,obs]
cat_arr = [cat,cat,cat]

connector = DummyApiConnector(addr, creds)

with open("./dummyDataset.json") as f:
    dummy_dataset = json.loads(f.read())

print("")
connector.dataset_exists('1')
print("")
connector.create_dataset('1', dummy_dataset)
print("")
print(connector.get_dataset_dimensions('1'))
print("")
connector.assign_dimensions_to_dataset('1', dims)
print("")
connector.append_dataset_observations('1', obs)
print("")
connector.overwrite_dataset_observations('1', obs_arr)
print("")
connector.variable_exists('1')
print("")
print(connector.get_variable_categories('1'))
print("")
connector.create_variable_category('1',cat_arr)
print("")
connector.update_variable_category('1','1',cat)

