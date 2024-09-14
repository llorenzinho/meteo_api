from functools import lru_cache

from pydantic_settings import BaseSettings

from app.core.config.log_config import LogConfig
from app.core.config.db_config import DatabaseConfig


class AppConfig(BaseSettings):
    http_interface: str = '0.0.0.0'
    http_port: int = 8000
    db_config: DatabaseConfig = DatabaseConfig()
    log_config: LogConfig = LogConfig()


@lru_cache
def get_config():
    return AppConfig()
