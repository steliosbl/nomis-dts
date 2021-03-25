from logging import getLogger
from pyjstat import pyjstat  # type: ignore
from abc import abstractmethod
logger = getLogger("DTS-Logger")


class DataSource:
    """
    This class represents the retrieval of data and returning it in the form of a pyjstat Dataset. The query() method
    has consciously been made abstract to allow for simpler configuration should another class inherit this class and is
    required to retrieve the data from a new source. Currently, this class is inherited by `CantabularApiConnector` and
    `DatasetFileReader`, with their query() methods customised to allow for retrieval of data via the Cantabular API and
    via local files, respectively.
    """

    @abstractmethod
    def query(self) -> pyjstat.Dataset:
        """
        Abstract method for either querying Cantabular directly, or generating a Cantabular-style jsonstat dataframe
        using the information from a local file; will be altered in accordingly by classes who inherit this.

        :return: A pyjstat Dataframe containing the query information (obtained via the load_jsonstat() method).
        """
        pass

    @staticmethod
    def load_jsonstat(data: str) -> pyjstat.Dataset:
        """
        Static method for taking a JSONstat string and returning a valid/verified pyjstat dataframe.

        :return: A pyjstat Dataframe containing the query information.
        """

        # Load response into a pyjstat dataframe.
        table = pyjstat.Dataset.read(data)

        if 'extension' not in table:
            raise ValueError("The file used to initialise the table does not represent a valid dataset.")

        # Report any categories in the rule variable that were blocked by disclosure control rules.
        blocked_categories = table['extension']['cantabular']['blocked']
        if blocked_categories:
            RULE_VAR_NAME, RULE_VAR = list(blocked_categories.items())[0]
            logger.info(f'The following categories of {RULE_VAR_NAME} failed disclosure control checks:',
                        ', '.join(RULE_VAR['category']['label'].values()))

        logger.debug("Data successfully loaded as a pyjstat dataframe.")
        return table
