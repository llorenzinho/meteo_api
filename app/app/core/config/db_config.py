from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    host: str = 'localhost'
    port: int = 3306
    user: str = 'user'
    password: str = 'password'
    database: str = 'db'

    model_config = SettingsConfigDict(env_prefix='db_')
