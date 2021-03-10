import logging
from type_hints import *


class Logger:
    """[Description]

    :param verbose:
    :type verbose: bool
    :param log_file:
    :type log_file: str
    """

    verbose: bool
    log_map: Dict[str, int]
    logger: logging.Logger

    def __init__(self, verbose: bool = False, log_file: str = "system.log") -> None:
        if log_file is None:
            log_file = "system.log"

        self.verbose = verbose
        self.log_map = {
            'CRITICAL': 50,
            'ERROR': 40,
            'WARNING': 30,
            'INFO': 20,
            'DEBUG': 10,
            'NOTSET': 0
        }

        self.logger = logging.getLogger('DTS-Logger')
        formatter = logging.Formatter(fmt='%(asctime)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, level: str, msg: str) -> None:
        self.logger.log(self.log_map[level], str(msg))
        if self.verbose:
            print(msg)
