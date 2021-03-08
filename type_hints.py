from typing import Union, Dict, List, Tuple, Any

NomisDataset = Dict[str, Union[str, bool, int, None]]
Variables = Dict[str, Union[str, bool, None]]
Dimensions = List[any]
Codes = List[str]
Observations = Dict[str, Union[str, Dimensions, Codes]]
