from type_hints import *
from logging import getLogger
logger = getLogger("DTS-Logger")


class Configuration:
    """Class to hold instances of Credentials and ConnectionInfo for all of the APIs that the program communicates with.

    :param config: A list of namedtuples containing instances of ConnectionInfo and Credentials for all APIs
    :ivar config: initial value: config
    """

    config: Dict[str, CredentialsConninfo]

    def __init__(self, config: Dict[str, CredentialsConninfo]) -> None:
        self.config = config

    def get_credentials(self, api: str) -> Tuple[str, str]:
        """Method for returning the credentials of a given API in the form of a tuple
        :param api: string representing the api credentials to receive: nomis, nomis_metadata, or cantabular
        :raises ValueError: if the api parameter is unknown
        :return: A tuple containing the username and password for the request API, respectively
        """
        try:
            return self.config[api.lower()].credentials.username, self.config[api.lower()].credentials.password
        except KeyError:
            raise ValueError(f"API {api} not recognised.")

    def get_client(self, api: str) -> str:
        """Method for returning the concatenation of an APIs address and port
        :param api: string representing the api to receive the client for: nomis, nomis_metadata, or cantabular
        :raises ValueError: if the api parameter is unknown
        :return: A string representing a concatenation of the address and the port, separated by a colon
        """
        try:
            if self.config[api.lower()].connection_info.port is not None:
                return str(f'{str(self.config[api.lower()].connection_info.address)}:'
                           f'{str(self.config[api.lower()].connection_info.port)}')
            else:
                return str(self.config[api.lower()].connection_info.address)
        except KeyError:
            raise ValueError(f"API {api} not recognised.")

    def get_geography(self) -> List[str]:
        try:
            return self.config["geography"]
        except KeyError:
            raise KeyError(f"Geography is not recognised")