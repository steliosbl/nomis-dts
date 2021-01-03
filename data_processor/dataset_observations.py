import numpy as np

class DatasetObservations:
    def __init__(self, table):
        self.table = table
        self.observations = []

    def observations_request(self):
        try:

            self.dataset_array = np.array(self.table["value"], dtype=np.int32).reshape([len(self.table["dimension"][self.d]["category"]["index"]) for self.d in self.table["dimension"]])
                
            # It is then possible to iterate over that array and print
            # values with the corresponding category labels.
            
            for self.index, self.count in np.ndenumerate(self.dataset_array):
                self.codes = []
                for self.i,self.v in enumerate(self.index):
                    self.code = (list(self.table["dimension"][list(self.table["dimension"])[self.i]]["category"]["index"])[self.v])
                    self.codes.append(self.code)
                
                self.names = []
                for self.dimension in self.table["dimension"]:
                    self.names.append(self.dimension)

                self.dimensions = []
                for self.code, self.name in zip(self.codes, self.names):
                    self.dimensions.append({
                        "name": self.name,
                        "code": self.code
                    })
                self.observations.append({
                    "dimensions": self.dimensions,
                    "observation": {
                        "value": self.count.item()
                    }
                    })

            return(self.observations)
            
        except:
            raise Exception("Error: Table Supplied is Null or Invalid")