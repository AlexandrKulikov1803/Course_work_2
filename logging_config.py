import logging
from typing import Any


def setup_logger(name: str, log_file: str, level: Any = logging.DEBUG) -> Any:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="w")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    return logger
