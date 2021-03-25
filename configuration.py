from type_hints import *
from logging import getLogger
logger = getLogger("DTS-Logger")


class Configuration:
    """
    Class to hold instances of Credentials and ConnectionInfo for all of the APIs that the program communicates with, in
    addition to the geography variables that must be considered when the program handles variables. This class is used
    frequently throughout the program, as it is the primary reference point as regards the program's settings for any
    given run.

    :param config: A list of `namedtuple`s containing instances of ConnectionInfo and Credentials for all APIs.
    :param var: Dictionary of special variables that must be acknowledged by the program.
    :ivar config: Initial value: config.
    :vartype config: Dict[str, CredentialsConninfo, List[str]]
    :ivar var: Initial value: var.
    :vartype var: Optional[Dict[List[str]]
    """

    config: Dict[str, CredentialsConninfo]
    var: Union[Dict[str, List[str]], None]

    def __init__(self, config: Dict[str, CredentialsConninfo], var: Dict[str, List[str]] = None) -> None:
        self.config = config
        self.var = var

    def get_credentials(self, api: str) -> Tuple[str, str]:
        """
        Method for returning the credentials for a given API in the form of a tuple. Convenient for more swift API
        authentication.

        :param api: String representing the API credentials to receive: nomis, nomis_metadata, or cantabular.
        :raises NameError: If the API name passed is not recognised by this instance.
        :return: A tuple containing the username and password for the request API, respectively.
        """
        try:
            return self.config[api.lower()].credentials.username, self.config[api.lower()].credentials.password
        except KeyError:
            raise ValueError(f"API {api} not recognised.")

    def get_client(self, api: str) -> str:
        """
        Method for returning the concatenation of the address and port of an API. Useful for more swift API connection.

        :param api: String representing the api to receive the client for: nomis, nomis_metadata, or cantabular.
        :raises NameError: If the API name passed is not recognised by this instance.
        :return: A string representing a concatenation of the address and the port, separated by a colon.
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
        """
        Method for returning a list of the geography variables that the program must consider.

        :raises KeyError: If the geography variables haven't been defined in the configuration.
        :return: The geography variables, as strings in a list.
        """
        try:
            if self.var is None:
                raise KeyError
            return self.var["geography"]
        except KeyError:
            raise KeyError(f"Geography is not recognised")
