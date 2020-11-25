from ipaddress import ip_address
from socket import gethostbyname
from urllib.parse import urlparse


class Credentials:  # sub-class of ApiConnectionInfo
    def __init__(self, username, password, key):
        self.username = username
        self.password = password
        self.key = key
        self.is_valid = None

    def validate(self) -> bool:
        """
        All attributes are mandatory; to validate, ensure all are valid strings.
        """
        if self.is_valid is not None:
            return self.is_valid

        self.is_valid = True

        try:
            if self.username is not None \
                    and isinstance(self.username, str):
                print("Username is valid.")
            else:
                raise Exception
        except:
            print("Username invalid, either none inputted or not a valid string.")
            self.is_valid = False

        try:
            if self.password is not None \
                    and isinstance(self.password, str):
                print("Password is valid.")
            else:
                raise Exception
        except:
            print("Password invalid, either none inputted or not a valid string.")
            self.is_valid = False

        try:
            if self.key is not None \
                    and isinstance(self.key, str):
                print("Key is valid.")
            else:
                raise Exception
        except:
            print("Key invalid, either none inputted or not a valid string.")
            self.is_valid = False

        return self.is_valid


class ConnectionInfo:   # sub-class of ApiConnectionInfo
    def __init__(self, api, address, port):
        try:
            self.address = ip_address(address)                      # First, checks if the inputted address is a valid IPv4 or IPv6 address, if so then store this and continue
        except ValueError:
            try:
                self.address = ip_address(gethostbyname(address))   # Next, it checks if the address is in the form www.website.co.uk (or .com, .org, etc). If so, then resolve this to an IP address, store and continue
            except:
                try:
                    urlinfo = urlparse(address)
                    if urlinfo.netloc != '':
                        self.address = ip_address(gethostbyname(urlinfo.netloc))    # If the inputted address is in the form http://www.website.com/path, then this will just grab the www.website.com part and resolve that to an ip address, store and continue
                    elif "/" in urlinfo.path:                                     # However, if the inputted address is in the form www.website.com/path (so, the same as above but without the http://, then we find the index where the path begins, remove this and resolve the www.website.com part to an ip address, store and continue
                        i = urlinfo.path.find("/")
                        self.address = ip_address(gethostbyname(urlinfo.path[0:i]))
                    else:
                        self.address = ip_address(gethostbyname(urlinfo.path))
                except:
                    self.address = address      # If all of the above fails, then we'll simply store the address exactly as it was inputted, and this will most likely go on to be invalid, and the default (localhost) will be used instead.
        try:
            self.port = int(port)
        except:
            self.port = port
        self.api = api
        self.is_valid = None
        if self.api == "Cantabular":
            self.default_port = "8491"
        else:
            self.default_port = "1234"  # Subject to change

    def validate(self) -> bool:
        """
        All attributes are mandatory; has defaults for address and port
        """
        if self.is_valid is not None:
            return self.is_valid

        self.is_valid = True

        try:
            ip_address(self.address)
            print(f"The address {self.address} is valid")
        except:
            print(f"The address {self.address} not valid. Using default, 127.0.0.1, instead.")
            self.address = "127.0.0.1"

        try:
            if 0 <= int(self.port) <= 49151:
                print(f"The port {self.port} is valid.")
            else:
                raise Exception
        except:
            print(f"The port {self.port} is not valid, using default, {self.default_port}, instead.")
            self.port = self.default_port

        return self.is_valid


class ApiConnectionInfo(Credentials, ConnectionInfo):
    def __init__(self, username, password, key, api, address, port):
        Credentials.__init__(self, username, password, key)
        ConnectionInfo.__init__(self, api, address, port)
