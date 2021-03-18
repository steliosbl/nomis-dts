from type_hints import *
from arguments import Arguments
import argparse
import sys


class ArgsManager:
    """Class for handling the input arguments, utilising the argparse library module. Allows for command line arguments
    in the form:
    - filename.py {metadata | data} -f {FILENAME (optional)} -q {QUERY in quotes} -i {ID} -t {TITLE} -y (for yes to all prompts) -v (for verbose)

    :ivar parser: An argparse ArgumentParser object for collecting arguments from the terminal
    """

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description='Data Transformation Service Census 2021'
        )
        self.parser.add_argument(
            "metadata",
            action='store',
            help='Toggle metadata mode.',
            type=str,
        )
        self.parser.add_argument(
            '-f',
            '--filename',
            action="store",
            help="Read data from a file instead of querying cantabular.",
            dest='filename',
            type=str,
            default=None
        )
        self.parser.add_argument(
            '-r',
            '--metadata-format',
            action="store",
            help="The format of the metadata E.g. 'C' ~ CANTABULAR, 'O' ~ ONS",
            dest='metadata_format',
            type=str,
            default=None
        )
        self.parser.add_argument(
            '-q'
            '--query-variables',
            action="store",
            help='delimited list input e.g. "COUNTRY, SEX"',
            dest='query_variables',
            type=str,
            default=None
        )
        self.parser.add_argument(
            '-i',
            '--dataset-id',
            action="store",
            help="nomis dataset ID e.g 'syn123'",
            dest='dataset_id',
            type=str,
            default=None
        )
        self.parser.add_argument(
            '-t',
            '--dataset-title',
            action="store",
            help='nomis dataset title e.g "TEST 1"',
            dest='dataset_title',
            type=str,
            default=None
        )
        self.parser.add_argument(
            '-d',
            '--query-dataset',
            action="store",
            help='the census dataset e.g. "Usual-Residents"',
            dest='query_dataset',
            type=str,
            default=None
        )
        self.parser.add_argument(
            '-y',
            '--suppress-prompts',
            action="store_true",
            help="suppresses all (y/n) prompts and automatically responds yes",
            default=False
        )
        self.parser.add_argument(
            '-v',
            '--verbose',
            action="store_true",
            help="verbose",
            default=False
        )
        self.parser.add_argument(
            '-c',
            '--config-file',
            action="store",
            help="path for non-default config file",
            type=str,
            default=None
        )
        self.parser.add_argument(
            '-l',
            '--log-file',
            action="store",
            help="path for non-default config file",
            type=str,
            default=None
        )

    def __enter__(self) -> 'ArgsManager':
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    def decode_arguments(self) -> 'Arguments':
        """Method for decoding the arguments collected by the parser into an instance of :class:Arguments, and then
        calling the :class:Arguments validate() method.

        :return: A validated instance of :class:Arguments corresponding with the terminal inputs
        """
        args = Arguments(self.parser.parse_args())
        args.validate()
        return args
