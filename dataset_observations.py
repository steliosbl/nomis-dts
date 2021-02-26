import numpy as np

class DatasetObservations:
    def __init__(self, table, dataset_id):
        self.table = table
        self.dataset_id = dataset_id
        self.dimensions = []
        self.codes = []

    def observations_request(self):
        try:

            for self.dimension in self.table["dimension"]:
                self.dimensions.append(self.dimension)
                self.codes.append(self.table["dimension"][self.dimension]["category"]["index"])

            return(
                {
                    "dataset": self.dataset_id,
                    "dimensions": self.dimensions,
                    "codes": self.codes,
                    "values": self.table["value"]
                }
            )
            
        except:
            raise Exception("Error: Table Supplied is Null or Invalid")