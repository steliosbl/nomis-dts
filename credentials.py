from type_hints import *
from logging import getLogger
logger = getLogger("DTS-Logger")


class Credentials:
    """Class for containing and validating API credentials

    :param username: A string of a valid username for accessing the associated API
    :param password: A string of a valid password for accessing the associated API
    :param key: A string of a valid key for accessing the associated API

    :ivar username: initial value: username
    :ivar password: initial value: username
    :ivar key: initial value: key
    """

    username: str
    password: str
    key: str

    def __init__(self, username: str, password: str, key: Union[str, None] = None) -> None:
        self.username = username
        self.password = password
        self.key = key

    def validate(self) -> bool:
        """Method for validating the Credentials class attributes. For this class, all attributes other than the key are
        mandatory, and so need to be successfully validated (in this case, they must all be valid, nonempty strings).
        Validation will still be successful if no key is passed.

        :return: True if validation is successful, otherwise an exception will have been raised
        """

        if not isinstance(self.username, str):
            raise TypeError("API credentials invalid; username must be a valid string. Please check the config file.")
        elif len(self.username) == 0:
            raise ValueError("API credentials invalid; username cannot be empty. Please check the config file.")
        else:
            logger.info(f"API username {self.username} is valid.")

        if not isinstance(self.password, str):
            raise TypeError("API credentials invalid; password must be a valid string. Please check the config file.")
        elif len(self.username) == 0:
            raise ValueError("API credentials invalid; password cannot be empty. Please check the config file.")
        else:
            logger.info(f"Password {self.password} is valid.")

        if self.key is None:
            logger.info("No key inputted.")
        elif not isinstance(self.key, str):
            raise TypeError("API credentials invalid; key must be a valid string. Please check the config file.")
        elif len(self.key) == 0:
            raise ValueError("API credentials invalid; a key, if included, it cannot be empty."
                             " Please check the config file.")

        # If no exception raised up to this point, then the credentials have been validated
        return True
