class DatasetObservations:
    def __init__(self, table):
        self.table = table
        self.observations = []

    def observations_request(self):
        try:
            self.dataset_array = np.array(self.table.counts, dtype=np.int32).reshape([len(self.d.labels) for self.d in self.table.dims])
                
            # It is then possible to iterate over that array and print
            # values with the corresponding category labels.
            
            for self.index, self.count in np.ndenumerate(self.dataset_array):
                self.codes = [self.table.dims[self.i].codes[self.v] for self.i,self.v in enumerate(self.index)]
                
                self.names = []
                for self.dimension in self.table.dims:
                    self.names.append(self.dimension.name)

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

            return(json.dumps(self.observations, indent=4))
            
        except:
            print("Error: Table Supplied is Null or Invalid")
            return(False)