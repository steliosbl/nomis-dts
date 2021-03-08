from type_hints import *
from pyjstat import pyjstat


class DatasetTransformations:
    """[Description]
    :param table:
    :type table:
    """
    def __init__(self, table: pyjstat.Dataset):
        self.table = table

    @staticmethod
    def dataset_creation(dataset_id: str, dataset_title: str) -> Union[NomisDataset, None]:
        """[Description]

        :param dataset_id:
        :type dataset_id: str
        :param dataset_title:
        :type dataset_title: str

        :raises Exception:

        :return: An initialised dataset...
        :rtype: dict|None
        """

        # This is just for testing purposes. Once we know the style of the IDs we can change this.
        # dataset_id should start with "syn" and end with a 5 digit number e.g. "syn01100".
        # dataset_title should be no longer than 10 characters long e.g. "Test 1".
        if dataset_id[0:3] == "syn":

            dataset = {
                "id": dataset_id,
                "title": dataset_title,
                "metadata": None,
                "contactId": None,
                "isAdditive": False,
                "isFlagged": False,
                "derivedFrom": None,
                "restrictedAccess": False,
                "minimumRound": 0,
                "online": True
                }
            return dataset
        else:
            raise Exception("Error: Table Supplied is Null or Invalid")

    def variable_creation(self) -> Union[List[Variables], None]:
        """[Description]
        :raises Exception:
        :return:
        :rtype:
        """
        requests = []
        try:
            for dimension in self.table["dimension"]:
                variable = {
                    "name": dimension,
                    "label": self.table["dimension"][dimension]["label"],
                    "metadata": None,
                    "defaults": self.table["dimension"][dimension]["category"]["index"]
                }
                requests.append(variable)

            return requests
        except:
            raise Exception("Error: Table Supplied is Null or Invalid")

    def category_creation(self) -> Union[List[Variables], None]:
        """
        :raises:
        :return:
        :rtype: list|None
        """
        requests = []
        try:
            for dimension in self.table["dimension"]:
                for label in self.table["dimension"][dimension]["category"]["label"]:
                    requests.append(
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

            return requests
        except:
            raise Exception("Error: Table Supplied is Null or Invalid")

    def assign_dimensions(self) -> Dimensions:
        """
        :raises:
        :return:
        :rtype:
        """
        requests = []
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
                requests.append(variable)

            return requests
        except:
            raise Exception("Error: Table Supplied is Null or Invalid")

    def observations(self, dataset_id: str) -> Union[Observations, None]:
        """[Description]

        :param dataset_id:
        :type dataset_id: str

        :raises Exception:
        :return:
        :rtype: list|None
        """
        dimensions = []
        codes = []
        try:

            for dimension in self.table["dimension"]:
                dimensions.append(dimension)
                codes.append(self.table["dimension"][dimension]["category"]["index"])

            return(
                {
                    "dataset": dataset_id,
                    "dimensions": dimensions,
                    "codes": codes,
                    "values": self.table["value"],
                    "statuses": None
                }
            )

        except:
            raise Exception("Error: Table Supplied is Null or Invalid")
