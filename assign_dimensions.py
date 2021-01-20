class AssignDimensions:
    def __init__(self, table):
        self.table = table
        self.requests = []

    def assign_dimensions_requests(self):
        try:
            for self.dimension in self.table["dimension"]:
                self.variable = {
                                    "name": self.dimension,
                                    "label": self.table["dimension"][self.dimension]["label"],
                                    "isAdditive": True,
                                    "variable": {
                                        "name": self.dimension,
                                        "view": None
                                    },
                                    "role": "measures",
                                    "canFilter": True,
                                    "defaults": self.table["dimension"][self.dimension]["category"]["index"],
                                    "database": {
                                        "isKey": False,
                                        "index": None,
                                        "defaultView": None,
                                        "discontinuities": None
                                    },
                                    "metadata": None
                                }
                self.requests.append(self.variable)

            return(self.requests)
        except:
            raise Exception("Error: Table Supplied is Null or Invalid")