from collections import namedtuple
from typing import (
    Union,
    Dict,
    List,
    Tuple,
    Any,
    Optional
)

""" 
File for containing all (custom) type hints or namedtuples used throughout the program
"""

NomisDataset = Dict[str, object]
Variables = Dict[str, object]
Dimensions = Dict[str, object]
Observations = Dict[str, object]
UuidMetadata = namedtuple("UuidMetadata", "uuid metadata")
CredentialsConninfo = namedtuple("CredentialsConninfo", "credentials connection_info")
