from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class LocalServerSettings(BaseSettings):
    HOST: str
    PORT: int

    model_config = SettingsConfigDict(env_prefix='LOCAL_SERVER_')


class SecretSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str


class DBSettings(BaseSettings):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: str
    NAME: str

    model_config = SettingsConfigDict(env_prefix='DB_')


class Settings(LocalServerSettings):
    local_server: LocalServerSettings
    secret: SecretSettings
    db: DBSettings

    model_config = SettingsConfigDict(env_file=f'{Path().absolute()}/.env')


settings = Settings()
