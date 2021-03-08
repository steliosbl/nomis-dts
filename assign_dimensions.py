from pyjstat import pyjstat
from type_hints import *


class AssignDimensions:
    """[Description]

    :param table:
    :type table:
    """
    def __init__(self, table: pyjstat.Dataset) -> None:
        self.table = table
        self.requests = []

    def assign_dimensions_requests(self) -> Dimensions:
        """
        :raises:
        :return:
        :rtype:
        """
        try:
            for dimension in self.table["dimension"]:
                variable = {
                    "name": dimension,
                    "label": self.table["dimension"][dimension]["label"],
                    "isAdditive": True,
                    "variable": {
                        "name": dimension,
                        "view": None
                    },
                    "role": "Measures",
                    "canFilter": True,
                    "defaults": self.table["dimension"][dimension]["category"]["index"],
                    "database": {
                        "isKey": False,
                        "index": 0,
                        "defaultView": None,
                        "discontinuities": None
                    },
                }
                self.requests.append(variable)

            return self.requests
        except:
            raise Exception("Error: Table Supplied is Null or Invalid")