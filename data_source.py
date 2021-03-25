from logging import getLogger
from pyjstat import pyjstat
from abc import abstractmethod
logger = getLogger("DTS-Logger")


class DataSource:
    """Class for reading and handling jsonstat dataframes
    """

    @abstractmethod
    def query(self) -> pyjstat.Dataset:
        """Abstract method for querying Cantabular; will be filled in accordingly by classes who inherit this
        """
        pass

    @staticmethod
    def load_jsonstat(data: str) -> pyjstat.Dataset:
        """Static method for taking a jsonstat string and returning a valid/verified pyjstat table
        """

        # Load response into a pyjstat dataframe.
        table = pyjstat.Dataset.read(data)

        # Report any categories in the rule variable that were blocked by disclosure control rules.
        blocked_categories = table['extension']['cantabular']['blocked']
        if blocked_categories:
            RULE_VAR_NAME, RULE_VAR = list(blocked_categories.items())[0]
            logger.info(f'The following categories of {RULE_VAR_NAME} failed disclosure control checks:',
                        ', '.join(RULE_VAR['category']['label'].values()))

        return table
