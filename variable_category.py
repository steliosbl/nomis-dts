from pyjstat import pyjstat
from type_hints import *


class VariableCategory:
    """[Description]

    :param table:
    :type table: pyjstat.Dataset
    """

    def __init__(self, table: pyjstat.Dataset) -> None:
        self.table = table
        self.requests = []

    def category_requests(self) -> Union[List[Variables], None]:
        """
        :raises:
        :return:
        :rtype: list|None
        """
        try:
            for dimension in self.table["dimension"]:
                for label in self.table["dimension"][dimension]["category"]["label"]:
                    self.requests.append(
                        {
                            "code": label,
                            "title": self.table["dimension"][dimension]["category"]["label"][label],
                            "ancestors": None,
                            "metadata": None,
                            "typeId": None,
                            "validity": {
                                "select": True,
                                "make": False
                            }
                        }
                    )

            return self.requests
        except:
            raise Exception("Error: Table Supplied is Null or Invalid")
