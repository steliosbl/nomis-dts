class Variable:
    def __init__(self, table):
        self.table = table
        self.requests = []

    def variable_requests(self):
        try:
            for self.dimension in self.table.dims:
                self.variable = {
                    "name": self.dimension.name,
                    "label": self.dimension.label,
                    "metadata": None,
                    "defaults": self.dimension.codes
                    }
                self.requests.append(self.variable)

            return(self.requests)
        except:
            raise exception("Error: Table Supplied is Null or Invalid")