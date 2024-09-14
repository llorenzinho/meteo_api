from logging import Logger, getLogger
from logging.config import dictConfig

from app.core.config.conf import get_config


def get_logger() -> Logger:
    dictConfig(get_config().log_config.model_dump())
    logger = getLogger(get_config().log_config.logger_name)
    return logger
