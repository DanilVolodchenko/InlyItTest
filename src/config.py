from typing_extensions import TypeAlias
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


SEC: TypeAlias = int

class Settings(BaseSettings):
    LOCAL_SERVER_HOST: str
    LOCAL_SERVER_PORT: int

    SECRET_KEY: str
    ALGORITHM: str

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    TOKEN_EXPIRED: SEC = 60 * 60 * 48

    @property
    def db_connection_string(self) -> str:
        return f'postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

    model_config = SettingsConfigDict(env_file=f'{Path().absolute()}/.env')


settings = Settings()
