class VariableCategory:
    def __init__(self, table):
        self.table = table
        self.requests = []

    def category_requests(self):
        try:
            for self.dimension in self.table.dims:
                for self.category, self.label in zip(self.dimension.codes, self.dimension.labels):
                    self.requests.append(
                        {
                        "code": self.category,
                        "title": self.label,
                        "ancestors": None,
                        "metadata": None,
                        "typeId": None,
                        "validity": {
                            "select": True,
                            "make": False
                            }
                        }
                    )

            return(json.dumps(self.requests, indent=4))
        except:
            print("Error: Table Supplied is Null or Invalid")
            return(False)