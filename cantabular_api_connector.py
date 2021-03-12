import requests
from pyjstat import pyjstat
from api_connector import ApiConnector
from data_source import DataSource
from logging import getLogger
logger = getLogger('DTS-Logger')


class CantabularApiConnector(ApiConnector, DataSource):
    """Class for communicating directly with the Cantabular API, in order to retrieve a jsonstat dataset based on
    specific queries.

    :param dataset: Name/ID of a dataset
    :param variables: A list containing valid variables.
    :ivar query_url: url with endpoints derived from params dataset and variables

    """
    def __init__(self, dataset: str, variables: list, credentials, address, port=None) -> None:
        super().__init__(credentials, address, port)

        # Construct the query url with endpoints using base url (client), dataset and variables.
        self.query_url = self.client + '/v8/query-json-stat/%s?%s' % (dataset, '&'.join([f'v={v}' for v in variables]))

    def query(self) -> pyjstat.Dataset:
        """Method for making a query to the Cantabular API using the argument variables.
        :raises requests.HTTPError: Raised in the case of a network partition or invalid query to the Cantabular API.
        :return: A cantabular table in the form of a jsonstat dataframe
        """
        try:
            res = self.session.get(self.query_url)
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Check for an errored response. This may occur if the query contained invalid values, or if the entire output
        # table was blocked for disclosure control reasons.
        if not res.ok:
            raise requests.HTTPError(f'HTTP error: {res.content}')

        # Load response into a pyjstat dataframe.
        return self.load_jsonstat(res.content.decode('utf-8'))
