import requests
from requests.auth import HTTPBasicAuth
from pyjstat import pyjstat
from type_hints import *


class CantabularConnector:
    """Class for communicating directly with the Cantabular API, in order to retrieve a jsonstat dataset based on
    specific queries.

    :param url: Valid url for connection to the Cantabular API
    :type url: str
    :param creds: Tuple containing a username and password for authenticating the Cantabular API
    :type creds: tuple
    """
    def __init__(self, url: str, creds: Tuple[str, str]) -> None:
        self.url = url
        self.creds = creds

        if len(self.creds) != 2:
            raise Exception('Invalid credentials file')

    def query(self, dataset: str, variables: list) -> pyjstat.Dataset:
        """Method for making a query to the Cantabular API using the argument variables.

        :param dataset: Name/ID of a dataset
        :type dataset: str

        :param variables: A list containing valid variables.
        :type variables: list

        :raises requests.HTTPError: Raised in the case of a network partition or invalid query to the Cantabular API.

        :return: A cantabular table in the form of a jsonstat dataframe.
        :rtype: pyjstat.Dataset
        """

        # Perform a query to query-json-stat endpoint using supplied BASE_URL,
        # DATASET and VARIABLES. The server is secured using HTTP Basic Authentication.
        QUERY = self.url + '/v8/query-json-stat/%s?%s' % (
            dataset, '&'.join([f'v={v}' for v in variables]))

        response = requests.get(QUERY, auth=HTTPBasicAuth(self.creds[0], self.creds[1]))

        # Check for an errored response. This may occur due to network issues, if the query
        # contained invalid values, or if the entire ouput table was blocked for disclosure
        # control reasons.
        if not response:
            raise requests.HTTPError(f'HTTP error: {response.content}')

        # Load response into a pystat dataframe.
        table = pyjstat.Dataset.read(response.content.decode('utf-8'))

        # Report any categories in the rule variable that were blocked by disclosure
        # control rules.
        self.blocked_categories = table['extension']['cantabular']['blocked']
        if self.blocked_categories:
            RULE_VAR_NAME, RULE_VAR = list(self.blocked_categories.items())[0]
            print(f'The following categories of {RULE_VAR_NAME} failed disclosure control checks:')
            print(', '.join(RULE_VAR['category']['label'].values()))
            print('')

        return table
