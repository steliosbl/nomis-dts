from api_connector import ApiConnector
from data_source import DataSource
from logging import getLogger
from pyjstat import pyjstat
import requests
logger = getLogger('DTS-Logger')


class CantabularApiConnector(ApiConnector, DataSource):
    """
    Class for communicating directly with the Cantabular API, in order to retrieve a jsonstat dataset based on
    specific queries. Currently only configured to work with data (i.e., not metadata).

    :param dataset: Name/ID of a dataset to retrieve from the Cantabular system.
    :param variables: A list containing valid variables.
    :ivar query_url: URL with endpoints derived from params dataset and variables.
    :vartype query_url: str

    """
    def __init__(self, dataset: str, variables: list, credentials, address, port=None) -> None:
        super().__init__(credentials, address, port)

        self.dataset = dataset
        self.variables = variables

        # Construct the query url with endpoints using base url (client), dataset and variables.
        self.query_url = self.client + '/v8/query-json-stat/%s?%s' % (dataset, '&'.join([f'v={v}' for v in variables]))

    def query(self) -> pyjstat.Dataset:
        """
        Method for making a query to the Cantabular API using the argument variables. This is the Cantabular API
            connector version of the query() abstract method, inherited from the `DataSource` class.

        :raises requests.HTTPError: Raised in the case of a network partition or invalid query to the Cantabular API.
        :return: A cantabular table in the form of a jsonstat dataframe.
        """
        try:
            logger.debug(f"Attempting to connect to the Cantabular API at {self.client}.")
            res = self.session.get(self.query_url)
            logger.info(f"Connection successfully established with the Cantabular API at {self.client}.")
        except Exception as e:
            raise requests.ConnectionError(f"Unable to connect to client. ({e})")

        # Check for an errored response. This may occur if the query contained invalid values, or if the entire output
        # table was blocked for disclosure control reasons.
        if res.status_code == 404:
            raise requests.HTTPError(f"Bad response from the Cantabular API: "
                                     f"the dataset '{self.dataset}' does not exist.")
        elif res.status_code == 400:
            raise requests.HTTPError(f'Bad response from the Cantabular API: the variables are either incorrect or'
                                     f'invalid. ({res.json()["message"]}.)')
        elif res.status_code == 401:
            raise requests.HTTPError(f'Bad response from the Cantabular API: the credentials were not accepted.'
                                     f'({res.json()["message"]}.)')
        elif not res.ok:
            raise requests.HTTPError(f'Bad response from the Cantabular API: {res.text}.')

        logger.info(f"{self.dataset} dataset with variables {self.variables} retrieved successfully.")

        # Load response into a pyjstat dataframe.
        return self.load_jsonstat(res.content.decode('utf-8'))
