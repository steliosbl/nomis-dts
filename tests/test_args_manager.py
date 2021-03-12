import sys
import unittest
from unittest.mock import patch
from args_manager import ArgsManager
from arguments import Arguments


class TestArgsManager(unittest.TestCase):
    def test_valid_args(self):
        args = [
            'prog',
            '-q', 'COUNTRY, SEX',
            '-d', 'Usual-Residents',
            '-i', 'DC1101EW',
            '-t', 'Dataset Title',
            '-y'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            arguments = args_manager.get_args()
            self.assertEqual(arguments.dataset_id, 'DC1101EW')
            self.assertEqual(arguments.dataset_title, 'Dataset Title')
            self.assertEqual(arguments.query_variables, ['COUNTRY', 'SEX'])
            self.assertEqual(arguments.query_dataset, 'Usual-Residents')
            self.assertTrue(arguments.suppress_prompts)
            self.assertFalse(arguments.verbose)

    def test_args_existing_files(self):
        args = [
            'prog',
            '-f', 'test_config.json',
            '-c', 'test_config.json',
            '-v'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            arguments = args_manager.get_args()
            self.assertEqual(arguments.dataset_id, None)
            self.assertEqual(arguments.dataset_title, None)
            self.assertEqual(arguments.query_variables, None)
            self.assertEqual(arguments.query_dataset, None)
            self.assertEqual(arguments.filename, 'test_config.json')
            self.assertEqual(arguments.config_file, 'test_config.json')
            self.assertFalse(arguments.suppress_prompts)
            self.assertTrue(arguments.verbose)
            self.assertIsInstance(arguments, Arguments)

    def test_args_nonexisting_files(self):
        args = [
            'prog',
            '-f', 'not-real.json'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            with self.assertRaises(OSError):
                args_manager.get_args()

    def test_insufficient_args(self):
        args = [
            'prog',
            # '-q', 'COUNTRY, SEX',
            '-d', 'Usual-Residents',
            '-i', 'DC1101EW',
            '-t', 'Dataset Title'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            with self.assertRaises(ValueError):
                args_manager.get_args()
        args = [
            'prog',
            '-q', 'COUNTRY, SEX',
            # '-d', 'Usual-Residents',
            '-i', 'DC1101EW',
            '-t', 'Dataset Title'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            with self.assertRaises(ValueError):
                args_manager.get_args()
        args = [
            'prog',
            '-q', 'COUNTRY, SEX',
            '-d', 'Usual-Residents',
            # '-i', 'DC1101EW',
            '-t', 'Dataset Title'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            with self.assertRaises(ValueError):
                args_manager.get_args()
        args = [
            'prog',
            '-q', 'COUNTRY, SEX',
            '-d', 'Usual-Residents',
            '-i', 'DC1101EW',
            # '-t', 'Dataset Title'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            with self.assertRaises(ValueError):
                args_manager.get_args()

    def test_invalid_args(self):
        args = [
            'prog',
            '-q', 'COUNTRY, , SEX',
            '-d', 'Usual-Residents',
            '-i', 'DC1101EW',
            '-t', 'Dataset Title'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            with self.assertRaises(ValueError):
                args_manager.get_args()


if __name__ == '__main__':
    unittest.main()
