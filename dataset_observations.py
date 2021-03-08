import numpy as np
from pyjstat import pyjstat
from type_hints import *


class DatasetObservations:
    """[Description]

    :param table:
    :type table: pyjstat.Dataset

    :param dataset_id:
    :type dataset_id: str
    """
    def __init__(self, table: pyjstat.Dataset, dataset_id: str) -> None:
        self.table = table
        self.dataset_id = dataset_id
        self.dimensions = []
        self.codes = []

    def observations_request(self) -> Union[Observations, None]:
        """[Description]

        :raises Exception:
        :return:
        :rtype: list|None
        """
        try:

            for self.dimension in self.table["dimension"]:
                self.dimensions.append(self.dimension)
                self.codes.append(self.table["dimension"][self.dimension]["category"]["index"])

            return(
                {
                    "dataset": self.dataset_id,
                    "dimensions": self.dimensions,
                    "codes": self.codes,
                    "values": self.table["value"],
                    "statuses": None
                }
            )

        except:
            raise Exception("Error: Table Supplied is Null or Invalid")
