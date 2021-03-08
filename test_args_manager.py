import sys
import unittest
from unittest.mock import patch
from args_manager import ArgsManager


class TestValidArgsManager(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_args = ['prog', 'query, variables', '-d', 'ds', '-v', '-y', '-i', 'syn001', '-t', 'title']
        self.valid_args_alt = ['prog', 'query, variables', '-f', './test.json', '-d', 'ds', '-i', 'syn001', '-t', 'title']

    def test_valid_args(self):
        with patch.object(sys, 'argv', self.valid_args):
            args_manager = ArgsManager()
            self.assertEqual(args_manager.dataset_id, 'syn001')
            self.assertEqual(args_manager.dataset_title, 'title')
            self.assertEqual(args_manager.query_variables, ['query', 'variables'])
            self.assertEqual(args_manager.query_dataset, 'ds')
            self.assertTrue(args_manager.y_flag)
        with patch.object(sys, 'argv', self.valid_args_alt):
            args_manager = ArgsManager()
            self.assertEqual(args_manager.dataset_id, 'syn001')
            self.assertEqual(args_manager.dataset_title, 'title')
            self.assertEqual(args_manager.query_variables, ['query', 'variables'])
            self.assertEqual(args_manager.query_dataset, 'ds')
            self.assertEqual(args_manager.file_name, './test.json')
            self.assertFalse(args_manager.y_flag)
            self.assertTrue(args_manager.use_file)


class TestInvalidArgsManager(unittest.TestCase):
    def setUp(self) -> None:
        self.invalid_args = ['prog', '-q', 88, 'syn001', 'title']

    def test_invalid_args(self):
        with patch.object(sys, 'argv', self.invalid_args):
            with self.assertRaises(TypeError):
                ArgsManager()


if __name__ == '__main__':
    unittest.main()
