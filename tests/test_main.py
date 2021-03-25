# type: ignore

import sys; sys.path.append('..')
from file_reader import FileReader
import logging
import unittest
from unittest.mock import patch
import main



"""
Prerequisites:
 - None

To run all tests:
 - python test_main.py

To run specific tests:   
 - python -m unittest test_main.TestMain.[test]
for instance,
 - python -m unittest test_main.TestMain.test_collect_arguments
 - python -m unittest test_main.TestMain.test_collect_configuration

Note: include -b flag to silence stdout
"""


class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        main.logger.setLevel(logging.ERROR)
        args = [
            'prog',
            'data',
            '-q', 'COUNTRY, SEX',
            '-d', 'Usual-Residents',
            '-i', 'DC1101EW',
            '-t', 'Dataset Title',
            '-c', 'test_config.json',
            '-y'

        ]
        with patch.object(sys, 'argv', args):
            self.arguments = main.collect_arguments()
        self.configuration = main.collect_configuration(self.arguments)

    def test_collect_arguments(self):
        args = [
            'prog',
            'data',
            '-q', 'COUNTRY, SEX',
            '-d', 'Usual-Residents',
            '-i', 'DC1101EW',
            '-t', 'Dataset Title',
            '-y'
        ]
        with patch.object(sys, 'argv', args):
            self.assertIsInstance(main.collect_arguments(), main.Arguments)

    def test_collect_configuration(self):
        self.assertIsInstance(main.collect_configuration(self.arguments), main.Configuration)




if __name__ == '__main__':
    unittest.main()
