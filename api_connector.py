from type_hints import *
import requests


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

    def __enter__(self) -> 'ApiConnector':
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        requests.Session.close(self.session)
