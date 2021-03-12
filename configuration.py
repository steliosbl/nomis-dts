from type_hints import *
from logging import getLogger
from credentials import Credentials
from connection_info import ConnectionInfo
logger = getLogger("DTS-Logger")


class Configuration:
    """Class to hold instances of Credentials and ConnectionInfo for all of the APIs that the program communicates with.

    :param cantabular_api_info: Connection information for the Cantabular API
    :param cantabular_api_credentials: Credentials for the Cantabular API
    :param nomis_api_info: Connection information for the Nomis API
    :param nomis_api_credentials: Credentials for the Nomis API
    :param nomis_metadata_api_info: Connection information for the Nomis metadata API
    :param nomis_metadata_api_credentials: Credentials for the Nomis metadata API

    :ivar cantabular_api_info: initial value: cantabular_api_info
    :ivar cantabular_api_credentials: initial value: cantabular_api_credentials
    :ivar nomis_api_info: initial value: nomis_api_info
    :ivar nomis_api_credentials: initial value: nomis_api_credentials
    :ivar nomis_metadata_api_info: initial value: nomis_metadata_api_info
    :ivar nomis_metadata_api_credentials: initial value: nomis_metadata_api_credentials
    """

    cantabular_api_info: ConnectionInfo
    cantabular_api_credentials: Credentials
    nomis_api_info: ConnectionInfo
    nomis_api_credentials: Credentials
    nomis_metadata_api_info: ConnectionInfo
    nomis_metadata_api_credentials: Credentials

    def __init__(self,
                 cantabular_api_info: ConnectionInfo, cantabular_api_credentials: Credentials,
                 nomis_api_info: ConnectionInfo, nomis_api_credentials: Credentials,
                 nomis_metadata_api_info: ConnectionInfo, nomis_metadata_api_credentials: Credentials,
                 ) -> None:
        self.cantabular_api_info = cantabular_api_info
        self.cantabular_api_credentials = cantabular_api_credentials
        self.nomis_api_info = nomis_api_info
        self.nomis_api_credentials = nomis_api_credentials
        self.nomis_metadata_api_info = nomis_metadata_api_info
        self.nomis_metadata_api_credentials = nomis_metadata_api_credentials

    def get_credentials(self, api: str) -> Tuple[str, str]:
        """Method for returning the credentials of a given API in the form of a tuple
        :param api: string representing the api credentials to receive: nomis, nomis_metadata, or cantabular
        :raises ValueError: if the api parameter is unknown
        :return: A tuple containing the username and password for the request API, respectively
        """
        if api.lower() == 'nomis':
            return self.nomis_api_credentials.username, self.nomis_api_credentials.password
        elif api.lower() == 'nomis_metadata':
            return self.nomis_metadata_api_credentials.username, self.nomis_metadata_api_credentials.password
        elif api.lower() == 'cantabular':
            return self.cantabular_api_credentials.username, self.cantabular_api_credentials.password
        else:
            raise ValueError(f"API {api} not recognised.")

    def get_client(self, api: str) -> str:
        """Method for returning the concatenation of an APIs address and port
        :param api: string representing the api to receive the client for: nomis, nomis_metadata, or cantabular
        :raises ValueError: if the api parameter is unknown
        :return: A string representing a concatenation of the address and the port, separated by a colon
        """
        if api.lower() == 'nomis':
            return str(f'{str(self.nomis_api_info.address)}:{str(self.nomis_api_info.port)}')
        elif api.lower() == 'nomis_metadata':
            return str(f'{str(self.nomis_metadata_api_info.address)}:{str(self.nomis_metadata_api_info.port)}')
        elif api.lower() == 'cantabular':
            return str(f'{str(self.cantabular_api_info.address)}:{str(self.cantabular_api_info.port)}')
        else:
            raise ValueError(f"API {api} not recognised.")
