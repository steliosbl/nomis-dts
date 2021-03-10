import logging
from type_hints import *


class Logger:
    verbose: bool
    log_map: Dict[str, int]

    def __init__(self, verbose: bool = False, log_file: str = "system.log") -> None:
            'CRITICAL': 50,
            'ERROR': 40,
            'WARNING': 30,
            'INFO': 20,
            'DEBUG': 10,
            'NOTSET': 0
        }
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s: %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )

    def log(self, level: str, msg: str) -> None:
        logging.log(self.log_map[level], str(msg))
        if self.verbose:
            print(msg)
