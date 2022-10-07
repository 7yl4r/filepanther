__version__ = "1.1.1"

from .util.config_logger import config_logger
config_logger()

from .parse import parse

__all__ = [
    "parse"
]
