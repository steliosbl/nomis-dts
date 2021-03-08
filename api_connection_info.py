from ipaddress import ip_address
from socket import gethostbyname
from urllib.parse import urlparse
from type_hints import *


class Credentials:
    """sub-class of ApiConnectionInfo

    :param username: A string of a valid username for accessing the associated API
    :type username: str
    :param password: A string of a valid password for accessing the associated API
    :type password: str
    :param key: A string of a valid key for accessing the associated API
    :type key: str, optional
    """
    def __init__(self, username: str, password: str, key: Union[str, None]) -> None:
        self.username = username
        self.password = password
        self.key = key
        self.is_valid = False

    def validate(self) -> bool:
        """Method for validating the Credentials class attributes. For this class, all attributes other than the key are
        mandatory, and so need to be successfully validated (in this case, they must all be valid strings). Validation
        will still be successful if no key is passed.

        :return: A bool indicating whether the validation has been successful (True) or not (False)
        :rtype: bool
        """

        self.is_valid = True

        try:
            if self.username is not None \
                    and isinstance(self.username, str):
                print("Username is valid.")
            else:
                raise TypeError
        except TypeError:
            print("Username invalid, either none inputted or not a valid string.")
            self.is_valid = False

        try:
            if self.password is not None \
                    and isinstance(self.password, str):
                print("Password is valid.")
            else:
                raise TypeError
        except TypeError:
            print("Password invalid, either none inputted or not a valid string.")
            self.is_valid = False

        try:
            if self.key is None:
                print("No key inputted.")
            elif isinstance(self.key, str):
                print("Key is valid.")
            else:
                raise TypeError
        except TypeError:
            print("Key invalid, either none inputted or not a valid string.")
            self.is_valid = False

        return self.is_valid


class ConnectionInfo:
    """sub-class of ApiConnectionInfo

    :param api: A string of the API for which this class contains connection information
    :type api: str
    :param address: A string of a valid address, either a url or IP address, for connecting to the API
    :type address: str
    :param port: A string or an integer representing the port the API will be served on
    :type port: str, int
    """
    def __init__(self, api: str, address: str, port: Union[str, int]) -> None:
        self.address = address
        try:
            # First, check if the inputted address is a valid IPv4 or IPv6 address, if so then store this and continue
            self.ip_address = ip_address(address)
        except ValueError:
            try:
                # Next, check if the address is in the form www.website.co.uk (or .com, .org, etc). If so, then \
                # resolve this to an IP address, store and continue
                self.ip_address = ip_address(gethostbyname(address))
            except:
                try:
                    urlinfo = urlparse(address)
                    if urlinfo.netloc != '':
                        # If the inputted address is in the form http://www.website.com/path, then this will just grab \
                        # the www.website.com part and resolve that to an ip address, store and continue
                        self.ip_address = ip_address(gethostbyname(urlinfo.netloc))
                    elif "/" in urlinfo.path:
                        # However, if the inputted address is in the form www.website.com/path (so, the same as above \
                        # but without the http://, then we find the index where the path begins, remove this and \
                        # resolve the www.website.com part to an ip address, store and continue
                        i = urlinfo.path.find("/")
                        self.ip_address = ip_address(gethostbyname(urlinfo.path[0:i]))
                    else:
                        self.ip_address = ip_address(gethostbyname(urlinfo.path))
                except:
                    # If all of the above fails, then we'll simply store the address exactly as it was inputted, \
                    # and this will most likely go on to be invalid, and the default (localhost) will be used instead.
                    self.ip_address = address
        try:
            self.port = str(port)
        except TypeError:
            self.port = "-1"
        self.api = api
        self.is_valid = False
        try:
            if self.api.lower() == "cantabular": self.default_port = "8491"
            elif self.api.lower() == "nomis":    self.default_port = "1234"   # Subject to change
            else: raise ValueError
        except ValueError:
            print("Unknown API; no default port set.")
            self.default_port = "-1"

    def validate(self) -> bool:
        """ Method for validating the ConnectionInfo attributes. For this class, all attributes are mandatory, and so
        need to be successfully validated. In this case, the api must be a valid string, the address must be a valid IP
        address, or must be able to be successfully resolved into one (i.e., it can be a valid URL), and port must be a
        valid numerical string, or an integer, and its numerical value must be within an acceptable range.

        :return: A bool indicating whether the validation has been successful (True) or not (False)
        :rtype: bool
        """

        self.is_valid = True

        try:
            ip_address(self.ip_address)
            print(f"The address {self.address} is valid")
        except:
            print(f"The address {self.address} not valid. Using default, 127.0.0.1, instead.")
            self.address = "localhost"

        try:
            if 0 <= int(self.port) <= 49151:
                print(f"The port {self.port} is valid.")
            else:
                raise Exception
        except:
            if self.default_port != "-1":
                print(f"The port {self.port} is not valid, using default, {self.default_port}, instead.")
                self.port = self.default_port
            else:
                print(f"The port {self.port} is not valid, and there is no default port.")
                self.is_valid = False

        return self.is_valid


class ApiConnectionInfo(Credentials, ConnectionInfo):
    """
    :param username: A string of a valid username for accessing the associated API
    :type username: str
    :param password: A string of a valid password for accessing the associated API
    :type password: str
    :param key: A string of a valid key for accessing the associated API
    :type key: str, optional
    :param api: A string of the API for which this class contains connection information
    :type api: str
    :param address: A string of a valid address, either a url or IP address, for connecting to the API
    :type address: str
    :param port: A string or an integer representing the port the API will be served on
    :type port: str, int
    """
    def __init__(self, username, password, key, api, address, port):
        Credentials.__init__(self, username, password, key)
        ConnectionInfo.__init__(self, api, address, port)

    def get_credentials(self) -> Tuple[str, str]:
        """
        :return: A tuple containing the username and password, respectively
        :rtype: Tuple[str, str]
        """
        return self.username, self.password

    def get_client(self) -> str:
        """
        :return: A string representing a concatenation of the address and the report, separated by a colon
        :rtype: str
        """
        return str(f'{str(self.address)}:{str(self.port)}')
