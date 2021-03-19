from file_reader import FileReader
from type_hints import *
from datetime import datetime
import requests
import json
import os


class ApiConnector:
    """Parent class for the three Api Connectors (namely, CantabularApiConnector, NomisApiConnector, and
    NomisMetadataApiConnector).

    :param address: A string of a valid address, either a url or IP address, for connecting to the API
    :param credentials: Contains the username and password for authentication with the API
    :param port: A string or an integer representing the port the API will be served on

    :ivar client: concatenation of the address and the port, if a port is included; otherwise, just the address
    :ivar session: a requests Session instance with authorisation for the associated API
    """

    client: str
    session: requests.Session

    def __init__(self, credentials: Tuple[str, str], address: str, port: Union[str, int, None]) -> None:
        self.client = f"{str(address)}:{str(port)}" if port is not None else str(address)
        self.session = requests.Session()
        self.session.auth = credentials
        self.this_instance = str(datetime.now().strftime("%Y%m%d-%H%M%S"))

    def __enter__(self) -> 'ApiConnector':
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        requests.Session.close(self.session)

    def save_request(self, method: str, res: Union[requests.Response, None]) -> None:
        """Method for saving requests and their responses to its own file

        :param method: The connector method within which the request was made
        :param res: The response received by the system
        """
        if res is None:
            request = "N/A"
            response = "N/A"
        else:
            request = "N/A" if res.request.body is None else json.dumps(json.loads(res.request.body), indent=4)
            try:
                response = json.dumps(res.json(), indent=4)
            except json.decoder.JSONDecodeError:
                response = "N/A"

        responses_directory = os.path.join('responses')
        if not os.path.exists(responses_directory):
            os.mkdir(responses_directory)

        this_response_directory = f'{responses_directory}/{self.this_instance}'
        if not os.path.exists(this_response_directory):
            os.mkdir(this_response_directory)

        file = f'{this_response_directory}/{datetime.now().strftime("%Y%m%d-%H%M%S")}_{method}.txt'
        file_data = '{}\n\n{}\n{}\n\nResponse Status Code: {}\n\nRequest Body: \n{}\n\nResponse Body: \n{}'.format(
                f'--------------------{method}--------------------',
                res.request.method + ' at ' + res.request.url,
                '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
                res.status_code,
                request,
                response
        )

        with FileReader(file) as fr:
            fr.write_text_file(file_data)
