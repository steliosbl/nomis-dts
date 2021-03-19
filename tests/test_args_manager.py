from unittest.mock import patch
from args_manager import ArgsManager
from arguments import Arguments
import unittest
import sys


class TestArgsManager(unittest.TestCase):
    def test_valid_args(self):
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
            args_manager = ArgsManager()
            arguments = args_manager.decode_arguments()
            self.assertEqual(arguments.dataset_id, 'DC1101EW')
            self.assertEqual(arguments.dataset_title, 'Dataset Title')
            self.assertEqual(arguments.query_variables, ['COUNTRY', 'SEX'])
            self.assertEqual(arguments.query_dataset, 'Usual-Residents')
            self.assertTrue(arguments.suppress_prompts)
            self.assertFalse(arguments.verbose)

    def test_args_existing_files(self):
        args = [
            'prog',
            'data',
            '-f', 'test_config.json',
            '-c', 'test_config.json',
            '-i', 'DC1101EW',
            '-t', 'Dataset Title',
            '-v'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            arguments = args_manager.decode_arguments()
            self.assertEqual(arguments.dataset_id, 'DC1101EW')
            self.assertEqual(arguments.dataset_title, 'Dataset Title')
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
            'data',
            '-c', 'test_config.json',
            '-i', 'DC1101EW',
            '-t', 'Dataset Title',
            '-f', 'not-real.json'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            with self.assertRaises(OSError):
                args_manager.decode_arguments()

    def test_insufficient_args(self):
        args = [
            'prog',
            'data',
            # '-q', 'COUNTRY, SEX',
            '-d', 'Usual-Residents',
            '-i', 'DC1101EW',
            '-t', 'Dataset Title'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            with self.assertRaises(ValueError):
                args_manager.decode_arguments()
        args = [
            'prog',
            'data',
            '-q', 'COUNTRY, SEX',
            # '-d', 'Usual-Residents',
            '-i', 'DC1101EW',
            '-t', 'Dataset Title'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            with self.assertRaises(ValueError):
                args_manager.decode_arguments()
        args = [
            'prog',
            'data',
            '-q', 'COUNTRY, SEX',
            '-d', 'Usual-Residents',
            # '-i', 'DC1101EW',
            '-t', 'Dataset Title'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            with self.assertRaises(ValueError):
                args_manager.decode_arguments()
        args = [
            'prog',
            'data',
            '-q', 'COUNTRY, SEX',
            '-d', 'Usual-Residents',
            '-i', 'DC1101EW',
            # '-t', 'Dataset Title'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            with self.assertRaises(ValueError):
                args_manager.decode_arguments()

    def test_invalid_args(self):
        args = [
            'prog',
            'data',
            '-q', 'COUNTRY, , SEX',
            '-d', 'Usual-Residents',
            '-i', 'DC1101EW',
            '-t', 'Dataset Title'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            with self.assertRaises(ValueError):
                args_manager.decode_arguments()
        args = [
            'prog',
            'invalid',
            '-q', 'COUNTRY',
            '-d', 'Usual-Residents',
            '-i', 'DC1101EW',
            '-t', 'Dataset Title'
        ]
        with patch.object(sys, 'argv', args):
            args_manager = ArgsManager()
            with self.assertRaises(ValueError):
                args_manager.decode_arguments()


if __name__ == '__main__':
    unittest.main()
