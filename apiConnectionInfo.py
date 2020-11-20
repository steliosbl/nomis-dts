class ConnectionInfo:   # sub-class of ApiConnectionInfo
    def __init__(self, cantabular_address, cantabular_port, nomis_address, nomis_port):
        self.cantabular_address = cantabular_address
        self.cantabular_port = cantabular_port
        self.nomis_address = nomis_address
        self.nomis_port = nomis_port
        self.is_valid = None

    def validate(self):
        """
        All attributes are mandatory; has defaults for address and port
        """
        if self.is_valid is not None:
            return self.is_valid

        self.is_valid = True

        try:
            if self.valid_address(self.cantabular_address) is not "Neither":
                print(f"The address {self.cantabular_address} is valid")
            else:
                raise Exception
        except:
            print(f"The address {self.cantabular_address} not valid. Using default, 127.0.0.1, instead.")
            self.cantabular_address = "127.0.0.1"

        try:
            if 0 <= int(self.cantabular_port) <= 49151:
                print(f"The port {self.cantabular_port} is valid.")
            else:
                raise Exception
        except:
            print(f"The port {self.cantabular_port} is not valid, using default, 8491, instead.")
            self.cantabular_port = "8491"

        try:
            if self.valid_address(self.nomis_address) is not "Neither":
                print(f"The address {self.nomis_address} is valid")
            else:
                raise Exception
        except:
            print(f"The address {self.nomis_address} not valid. Using default, 127.0.0.1, instead.")
            self.nomis_address = "127.0.0.1"

        try:
            if 0 <= int(self.nomis_port) <= 49151:
                print(f"The port {self.nomis_port} is valid.")
            else:
                raise Exception
        except:
            print(f"The port {self.nomis_port} is not valid, using default, 1234, instead.")
            self.nomis_port = "8491"

        return self.is_valid

    def valid_address(self, IP):  # Stolen from https://www.tutorialspoint.com/validate-ip-address-in-python
        """
        :type IP: str
        :rtype: str
        """
        def isIPv4(s):
            try:
                return str(int(s)) == s and 0 <= int(s) <= 255
            except:
                return False
        def isIPv6(s):
            if len(s) > 4:
                return False
            try:
                return int(s, 16) >= 0 and s[0] != '-'
            except:
                return False
        if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
            return "IPv4"
        if IP.count(":") == 7 and all(isIPv6(i) for i in IP.split(":")):
            return "IPv6"
        return "Neither"


class Credentials:  # sub-class of ApiConnectionInfo
    def __init__(self, username, password, key):
        self.username = username
        self.password = password
        self.key = key
        self.is_valid = None

    def validate(self):
        if self.username is None:
            print("Username invalid, none inputted.")
            self.is_valid = False

        if self.password is None:
            print("Password invalid, none inputted.")
            self.is_valid = False

        if self.key is None:
            print("Key invalid, none inputted.")
            self.is_valid = False

        return self.is_valid


class ApiConnectionInfo:  # WIP
    def __init__(self, cantabular_address, cantabular_port, nomis_address, nomis_port, username, password, key):
        self.cantabular_address = cantabular_address
        self.cantabular_port = cantabular_port
        self.nomis_address = nomis_address
        self.nomis_port = nomis_port
        self.username = username
        self.password = password
        self.key = key
