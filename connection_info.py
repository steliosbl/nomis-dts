from urllib.parse import urlparse
from type_hints import *
from ipaddress import ip_address
from logging import getLogger
from socket import gethostbyname, gaierror

logger = getLogger("DTS-Logger")


class ConnectionInfo:
    """Class for containing and validating the connection information (address and port) for each API

    :param address: A string of a valid address, either a url or IP address, for connecting to the API
    :param port: A string or an integer representing the port the API will be served on

    :ivar address: initial value: address
    :ivar port: initial value: port

    """

    address: str
    port: Union[str, int]

    def __init__(self, address: str, port: Union[str, int, None]) -> None:
        self.address = address
        self.port = port

    def validate(self) -> bool:
        """ Method for validating the ConnectionInfo attributes. For this class, all attributes are mandatory, and so
        need to be successfully validated. In this case, the address must be a valid IP address, or must be able to be
        successfully resolved into one (i.e., it can be a valid URL), and port must be a valid numerical string, or an
        integer, and its numerical value must be within an acceptable range.

        :return: True if the validation is successful; otherwise, an exception will have been raised.
        """
        if not isinstance(self.address, str):
            raise TypeError("API connection information failed to validate; the address must be a valid string. Please "
                            "check the config file.")
        elif len(self.address) == 0:
            raise ValueError("API connection information failed to validate; the address cannot be empty. Please check "
                             "the config file.")

        try:
            # First, check if the inputted address is a valid IPv4 or IPv6 address, if so then store this and continue
            ip_address(self.address)
        except ValueError:
            try:
                # Next, check if the address is in the form www.website.co.uk (or .com, .org, etc). If so, then \
                # resolve this to an IP address, store and continue
                ip_address(gethostbyname(self.address))
            except gaierror:
                try:
                    urlinfo = urlparse(self.address)
                    if urlinfo.netloc != '':
                        # If the inputted address is in the form http://www.website.com/path, then this will just grab \
                        # the www.website.com part and resolve that to an ip address, store and continue
                        ip_address(gethostbyname(urlinfo.netloc))
                    elif "/" in urlinfo.path:
                        # However, if the inputted address is in the form www.website.com/path (so, the same as above \
                        # but without the http://, then we find the index where the path begins, remove this and \
                        # resolve the www.website.com part to an ip address, store and continue
                        ip_address(gethostbyname(urlinfo.path[0:urlinfo.path.find("/")]))
                    else:
                        ip_address(gethostbyname(urlinfo.path))
                except ValueError:
                    # If all of the above fails, then we can safely say the inputted address is not valid
                    raise ValueError("API connection info invalid; inputted address cannot be resolved. Please check"
                                     "the config file.")
        logger.info(f"The address {self.address} is valid.")

        if self.port is None:
            logger.info("No port inputted.")
        elif not isinstance(self.port, str) and not isinstance(self.port, int):
            raise TypeError("API connection information failed to validate; the port must be a valid integer or "
                            "numeric string. Please check the config file.")
        elif not 0 <= int(self.port) <= 49151:
            raise ValueError("API connection information failed to validate; port is out of range. Please check the "
                             "config file.")
        else:
            self.port = str(self.port)
            logger.info(f"Port {self.port} is valid.")

        return True
