class Variable:
    def __init__(self, table):
        self.table = table
        self.requests = []

    def variable_requests(self):
        try:
            for self.dimension in self.table["dimension"]:
                self.variable = {
                    "name": self.dimension,
                    "label": self.table["dimension"][self.dimension]["label"],
                    "metadata": None,
                    "defaults": self.table["dimension"][self.dimension]["category"]["index"]
                    }
                self.requests.append(self.variable)

            return(self.requests)
        except:
            raise Exception("Error: Table Supplied is Null or Invalid")