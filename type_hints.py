from collections import namedtuple
from typing import (
    Union,
    Dict,
    List,
    Tuple,
    Any
)

""" 
File for containing all (custom) type hints or namedtuples used throughout the program
"""

NomisDataset = Dict[str, Union[str, bool, int, None]]
Variables = Dict[str, Union[str, bool, None]]
Dimensions = Dict[any, any]
Codes = List[str]
Observations = Dict[str, Union[str, Dimensions, Codes]]
UuidMetadata = namedtuple("uuid_metadata", "uuid metadata")
CredentialsConninfo = namedtuple("credentials_conninfo", "credentials connection_info")
