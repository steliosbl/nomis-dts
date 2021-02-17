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
                                    "role": "Measures",
                                    "canFilter": True,
                                    "defaults": self.table["dimension"][self.dimension]["category"]["index"],
                                    "database": {
                                        "isKey": False,
                                        "index": 0,
                                        "defaultView": None,
                                        "discontinuities": None
                                    },
                                    "uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                                }
                self.requests.append(self.variable)

            return(self.requests)
        except:
            raise Exception("Error: Table Supplied is Null or Invalid")