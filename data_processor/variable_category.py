class VariableCategory:
    def __init__(self, table):
        self.table = table
        self.requests = []

    def category_requests(self):
        try:
            for self.dimension in self.table["dimension"]:
                for self.label in self.table["dimension"][self.dimension]["category"]["label"]:
                    self.requests.append(
                        {
                        "code": self.label,
                        "title": self.table["dimension"][self.dimension]["category"]["label"][self.label],
                        "ancestors": None,
                        "metadata": None,
                        "typeId": None,
                        "validity": {
                            "select": True,
                            "make": False
                            }
                        }
                    )

            return(self.requests)
        except:
            raise Exception("Error: Table Supplied is Null or Invalid")