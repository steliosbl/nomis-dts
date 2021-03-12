from type_hints import *
import json
import os


class FileReader:
    """Class for handling files; reading, writing, and checking for existence

    :param file: a string representing the location of a file for use in the program
    :ivar: initial value: file
    """

    file: str

    def __init__(self, file: str) -> None:
        self.file = file

    def __enter__(self) -> 'FileReader':
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    def exists(self) -> bool:
        if not os.path.exists(self.file):
            raise FileNotFoundError(f"The file {self.file} could not be located.")
        else:
            return True

    def load_json(self) -> Union[dict, str]:
        with open(self.file) as json_file:
            data = json.loads(json_file.read())
        return data

    def write_json(self, to_write: str) -> None:
        with open(self.file, 'w') as f:
            json.dump(to_write, f, indent=2)
