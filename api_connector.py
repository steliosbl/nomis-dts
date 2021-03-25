from file_reader import FileReader
from type_hints import *
from datetime import datetime
from logging import getLogger
import requests
import json
import os
logger = getLogger("DTS-Logger")


class ApiConnector:
    """
    Parent class for the three Api Connectors (namely, CantabularApiConnector, NomisApiConnector, and
    NomisMetadataApiConnector).

    :param address: A string of a valid address, either a url or IP address, for connecting to the API.
    :param credentials: Contains the username and password for authentication with the API.
    :param port: A string or an integer representing the port the API will be served on.

    :ivar client: Concatenation of the address and the port, if a port is included; otherwise, just the address.
    :vartype client: str
    :ivar session: A requests Session instance with authorisation for the associated API.
    :vartype session: Session
    :ivar record_requests: Boolean toggle, when set to `True` the save_request() method will permitted, whereas when
        set to `False`, it will be prohibited.
    :vartype record_requests: bool
    """

    # client: str
    # session: requests.Session

    def __init__(self, credentials: Tuple[str, str], address: str, port: Union[str, int, None],
                 record_requests: bool = True) -> None:
        self.client = f"{str(address)}:{str(port)}" if port is not None else str(address)
        self.session = requests.Session()
        self.session.auth = credentials
        self.this_instance = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
        self.record_requests = record_requests

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        requests.Session.close(self.session)

    def save_request(self, method: str, res: requests.Response) -> None:
        """
        Method for saving requests made and their responses (success or failure) to distinct files. Each created file
        will reside within a directory specific to this particular API connector instance.

        :param method: The connector method within which the request was made.
        :param res: The response received by the system.
        """
        if not self.record_requests:
            return

        request = "N/A" if res.request.body is None else json.dumps(json.loads(res.request.body), indent=4)
        try:
            response = json.dumps(res.json(), indent=4)
        except ValueError:
            response = "N/A"

        responses_directory = os.path.join('responses')
        if not os.path.exists(responses_directory):
            os.mkdir(responses_directory)

        this_response_directory = f'{responses_directory}/{self.this_instance}'
        if not os.path.exists(this_response_directory):
            os.mkdir(this_response_directory)

        if isinstance(res, requests.Response):
            file = f'{this_response_directory}/{datetime.now().strftime("%Y%m%d-%H%M%S")}_{method}.txt'
            file_data = '{}\n\n{}\n{}\n\nResponse Status Code: {}\n\nRequest Body: \n{}\n\nResponse Body: \n{}'.format(
                    f'--------------------{method}--------------------',
                    f'{str(res.request.method)} at {str(res.request.url)}',
                    '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
                    res.status_code,
                    request,
                    response
            )

        logger.debug(f"Writing request for method {method} to file {file}.")
        with FileReader(file) as fr:
            fr.write_text_file(file_data)
