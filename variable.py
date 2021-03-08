from pyjstat import pyjstat
from type_hints import *


class Variable:
    """[Description]
    :param table:
    :type table:
    """

    def __init__(self, table: pyjstat.Dataset) -> None:
        self.table = table
        self.requests = []

    def variable_requests(self) -> Union[List[Variables], None]:
        """[Description]
        :raises Exception:
        :return:
        :rtype:
        """
        try:
            for self.dimension in self.table["dimension"]:
                variable = {
                    "name": self.dimension,
                    "label": self.table["dimension"][self.dimension]["label"],
                    "metadata": None,
                    "defaults": self.table["dimension"][self.dimension]["category"]["index"]
                    }
                self.requests.append(variable)

            return self.requests
        except:
            raise Exception("Error: Table Supplied is Null or Invalid")
