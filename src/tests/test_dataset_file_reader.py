# type: ignore

import sys; sys.path.append('..')
import unittest
from pyjstat import pyjstat
from dataset_file_reader import DatasetFileReader

"""
Prerequisites:
 - None

To run all tests:
 - python test_dataset_file_reader.py

To run specific tests:   
 - python -m unittest test_dataset_file_reader.TestDatasetFileReader.[test]
for instance,
 - python -m unittest test_dataset_file_reader.TestDatasetFileReader.test_valid_file
 - python -m unittest test_dataset_file_reader.TestDatasetFileReader.test_nonexisting_file

Note: include -b flag to silence stdout
"""

VALID_FILE = 'test_dataset_file.json'
INVALID_FILE_1 = 'not_real.json'
INVALID_FILE_2 = 'test_config.json'


class TestDatasetFileReader(unittest.TestCase):

    def test_valid_file(self) -> None:
        with DatasetFileReader(VALID_FILE) as dfr:
            self.assertIsInstance(dfr.query(), pyjstat.Dataset)

    def test_nonexisting_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            with DatasetFileReader(INVALID_FILE_1) as dfr:
                dfr.query()

    def test_invalid_file(self) -> None:
        with self.assertRaises(ValueError):
            with DatasetFileReader(INVALID_FILE_2) as dfr:
                dfr.query()


if __name__ == '__main__':
    unittest.main()
