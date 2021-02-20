from logging import config
import logging
from typing import TypeVar, Union
import yaml

from rest_framework import status
from rest_framework.exceptions import force_str

from django.utils.translation import gettext_lazy as _

from .logging_settings import (
    DEFAULT_LOGGER_NAME, DEFAULT_LOG_CONFIG_FILE
)


# Types
file_path = Union[str, int, bytes]
log_config_type = TypeVar("log_config_type", dict, file_path)


class ApplicationErrors(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = _('An application error occurred.')
    default_code = 'error'
    log_config: log_config_type = DEFAULT_LOG_CONFIG_FILE    # log config file or dict

    def __init__(
            self, message=None, code=None, logger_name: str = None,
            **err_dict_kwargs
    ):
        if message is None:
            message = force_str(self.default_message)
        if code is None:
            code = self.default_code
        if logger_name is None:
            logger_name = DEFAULT_LOGGER_NAME

        self.message, self.code = message, code
        self.logger = logger_name
        # Used to build error dict for rest framework
        self.error_dict_kwargs = err_dict_kwargs

    def __str__(self):
        return str(self.message)

    @classmethod
    def err_type(cls) -> str:
        return cls.__name__

    # Error dict for rest framework
    def err_dict(self):
        dict_ = {
            "error": {
                "type": self.err_type(),
                "message": self.message,
                "code": self.code,
                **self.error_dict_kwargs
            }
        }
        return dict_

    # Override to return a dict containing extra_kwargs for logging
    def extra_kwargs(self) -> dict:
        return {}

    def _extra_kwargs(self) -> dict:
        dic = self.extra_kwargs()
        if self.log_config == DEFAULT_LOG_CONFIG_FILE:
            dic.update({"err_type": self.err_type()})
        return dic

    def get_logger(self) -> logging.Logger:
        log_config = __class__.log_config
        if isinstance(log_config, dict):
            config.dictConfig(log_config)
        else:
            with open(log_config, "r") as file:
                config_ = yaml.safe_load(file.read())
                config.dictConfig(config_)
        return logging.getLogger(self.logger)








