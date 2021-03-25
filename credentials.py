from type_hints import *
from logging import getLogger
logger = getLogger("DTS-Logger")


class Credentials:
    """
    Class for containing and validating API credentials.

    :param username: A string containing a valid username for authenticating the associated API.
    :param password: A string containing a valid password for authenticating the associated API.
    :param key: A string containing a valid key for accessing the associated API.

    :ivar username: Initial value: `username`.
    :vartype username: str
    :ivar password: Initial value: `password`.
    :vartype password: str
    :ivar key: Initial value: `key`.
    :vartype key: Optional[str]
    """

    username: str
    password: str
    key: str

    def __init__(self, username: str, password: str, key: Union[str, None] = None) -> None:
        self.username = username
        self.password = password
        self.key = key

    def validate(self) -> bool:
        """
        Method for validating the Credentials class attributes. For this class, all attributes other than the `key` are
        mandatory, and so need to be successfully validated (in this case, they must all be valid, nonempty strings).
        Validation will still be successful if no key is passed.

        :raises TypeError: If any of the `username`, `password`, or `key` (if not `None`) are not valid strings.
        :raises ValueError: If the `username`, `password`, or `key` (if not `None`) are empty strings.
        :return: `True` if validation is successful, otherwise an exception will have been raised.
        """

        if not isinstance(self.username, str):
            raise TypeError("API credentials invalid; username must be a valid string. Please check the config file.")
        elif len(self.username) == 0:
            raise ValueError("API credentials invalid; username cannot be empty. Please check the config file.")
        else:
            logger.debug(f"API username {self.username} is valid.")

        if not isinstance(self.password, str):
            raise TypeError("API credentials invalid; password must be a valid string. Please check the config file.")
        elif len(self.username) == 0:
            raise ValueError("API credentials invalid; password cannot be empty. Please check the config file.")
        else:
            logger.debug(f"Password {self.password} is valid.")

        if self.key is None:
            logger.debug("No key inputted.")
        elif not isinstance(self.key, str):
            raise TypeError("API credentials invalid; key must be a valid string. Please check the config file.")
        elif len(self.key) == 0:
            raise ValueError("API credentials invalid; a key, if included, it cannot be empty."
                             " Please check the config file.")

        # If no exception raised up to this point, then the credentials have been validated
        return True
