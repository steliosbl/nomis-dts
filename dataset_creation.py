from type_hints import *


class DatasetCreation:
    """[Description]

    :param dataset_id:
    :type dataset_id: str

    :param dataset_title:
    :type dataset_title: str
    """
    def __init__(self, dataset_id: str, dataset_title: str) -> None:
        self.dataset_id = dataset_id
        self.dataset_title = dataset_title

    def dataset_request(self) -> Union[NomisDataset, None]:
        """[Description]

        :raises Exception:

        :return: An initialised dataset...
        :rtype: dict|None
        """

        # This is just for testing purposes. Once we know the style of the IDs we can change this.
        # dataset_id should start with "syn" and end with a 5 digit number e.g. "syn01100".
        # dataset_title should be no longer than 10 characters long e.g. "Test 1".
        if self.dataset_id[0:3] == "syn":

            dataset = {
                "id": self.dataset_id,
                "title": self.dataset_title,
                "metadata": None,
                "contactId": None,
                "isAdditive": False,
                "isFlagged": False,
                "derivedFrom": None,
                "restrictedAccess": False,
                "minimumRound": 0,
                "online": True
                }
            return dataset
        else:
            raise Exception("Error: Table Supplied is Null or Invalid")
