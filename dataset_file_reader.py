from pyjstat import pyjstat
from logging import getLogger
from data_source import DataSource
from file_reader import FileReader
logger = getLogger('DTS-Logger')


class DatasetFileReader(FileReader, DataSource):
    """[Description]
    """
    def __init__(self, file: str) -> None:
        super().__init__(file)

    def query(self) -> pyjstat.Dataset:
        """[Description]
        :raises FileNotFoundError: If the input file path can't be located

        :return: A cantabular table in the form of a jsonstat dataframe
        """
        self.exists()
        return self.load_jsonstat(self.load_json())


# EXAMPLE

# read_from_file = readFromFile("query_file_example.json")
# table = read_from_file.read()
# logger.info(table)
