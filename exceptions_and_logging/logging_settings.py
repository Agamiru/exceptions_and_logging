import logging
import os

EXTRA_KWARGS = ["err_type"]
DEFAULT_LOGGER_NAME = "default_logger"
MSG_FORMAT = '%(asctime)s - APPLICATION ERROR - %(levelname)s\n' \
             'Error Type: %(err_type)s\n' \
             'Error Message: %(message)s\n'

module_dir = os.path.dirname(__file__)
DEFAULT_LOG_CONFIG_FILE = os.path.join(module_dir, "logging_config.yaml")


class DefaultFormatter(logging.Formatter):
    """
    Default message formatter. Adds extra double lines for readability.
    """

    def __init__(
            self, fmt=MSG_FORMAT,
            datefmt='%m/%d/%Y %I:%M:%S %p'
    ):
        super().__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record):
        s = super().format(record)
        return s + "\n" * 2


default_dict_config = {
    "version": 1,

    "formatters": {
        "default": {
            "()": DefaultFormatter,
            "format": MSG_FORMAT,
        }
    },
    "handlers": {
        "console": {
            "class": 'logging.StreamHandler',
            "formatter": "default"
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": "application.log",
            "encoding": "utf-8"
        }
    },

    "loggers": {
        DEFAULT_LOGGER_NAME: {
            "level": "ERROR",
            "handlers": ["console", "file"]
        },
    },

    'root': {
        'level': 'DEBUG',
        'handlers': ["console"]
    },
}
