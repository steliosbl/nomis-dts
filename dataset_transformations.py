from type_hints import *
from pyjstat import pyjstat


class DatasetTransformations:
    """Class containing methods for transforming the data retrieved from Cantabular

    :param table: a pyjstat dataframe containing the data to be used/transformed
    :ivar table: initial value: table
    """
    def __init__(self, table: pyjstat.Dataset):
        self.table = table

    @staticmethod
    def dataset_creation(dataset_id: str, dataset_title: str) -> NomisDataset:
        """Method for initialising a Nomis-style dataset using an inputted ID and title.

        :param dataset_id: A valid string representing the ID of the dataset to be created
        :param dataset_title: A valid string representing the title of the dataset to be created

        :raises TypeError: If dataset_id or dataset_title are not valid strings (str types)
        :raises ValueError: If dataset_id or dataset_title have a length of 0 (i.e., are empty)

        :return: If no exception is raised, an initialised dataset as a Python dict with valid keys and values
        """
        if not isinstance(dataset_id, str):
            raise TypeError(f"The dataset id (inputted: {dataset_id}) must be a string.")
        if not isinstance(dataset_title, str):
            raise TypeError(f"The dataset id (inputted: {dataset_title}) must be a string.")
        if len(dataset_id) == 0:
            raise ValueError(f"The dataset id must not be empty.")
        if len(dataset_title) == 0:
            raise ValueError(f"The dataset title must not be empty.")

        ds = {
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
        return ds

    def variable_creation(self) -> List[Variables]:
        """Method for converting the variable data from the pyjstat dataframe into valid variables for communication
        with the Nomis API

        :raises KeyError: If the dataframe doesn't contain any dimension information
        :return:
        """
        if "dimension" not in self.table:
            raise KeyError("Table supplied contains no dimensions key.")

        requests = []
        for dimension in self.table["dimension"]:
            variable = {
                "name": dimension,
                "label": self.table["dimension"][dimension]["label"],
                "metadata": None,
                "defaults": self.table["dimension"][dimension]["category"]["index"]
            }
            requests.append(variable)

        return requests

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
