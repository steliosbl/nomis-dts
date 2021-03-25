from data_source import DataSource
from file_reader import FileReader
from logging import getLogger
from pyjstat import pyjstat
import json
logger = getLogger('DTS-Logger')


class DatasetFileReader(FileReader, DataSource):
    """
    Class for handling datasets read from files locally rather than queried directly from Cantabular. Inherits from
    `DataSource` with its query() method configured for the retrieval of data from local files, and the `FileReader`
    class is also inherited to assist with this retrieval (and verification).
    """
    def __init__(self, file: str) -> None:
        super().__init__(file)

    def query(self) -> pyjstat.Dataset:
        """
        The file equivalent of querying cantabular; i.e., ensuring the inputted file exists and converting it into
        a usable pyjstat Dataset (table).

        :raises FileNotFoundError: If the input file path can't be located.
        :return: A cantabular table in the form of a jsonstat dataframe.
        """
        self.exists()
        logger.info(f"Reading data locally from the file: {self.file}.")
        return self.load_jsonstat(json.dumps(self.load_json()))
