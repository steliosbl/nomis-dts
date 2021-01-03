class DatasetCreation:
    def __init__(self, dataset_id, dataset_title):

        self.dataset_id = dataset_id
        self.dataset_title = dataset_title

    def dataset_request(self):

        #This is just for testing purposes. Once we know the style of the IDs we can change this.
        #dataset_id should start with "syn" and end with a 5 digit number e.g. "syn01100".
        #dataset_title should be no longer than 10 characters long e.g. "Test 1".
        if dataset_id[0:3] == "syn" and len(dataset_id) == 8 and len(dataset_title) <= 10:

            self.dataset = {
                "id": self.dataset_id,
                "title": self.dataset_title,
                "metadata": None,
                "contactId": None,
                "isAdditive": False,
                "isFlagged": False,
                "derivedFrom": None,
                "restrictedAccess": False,
                "online": True
                }
            return(self.dataset)
        else:
            raise Exception("Error: Table Supplied is Null or Invalid")