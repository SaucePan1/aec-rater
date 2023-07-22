"""Environment settings."""

from pathlib import Path

from pydantic import DirectoryPath, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Product rater settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PATH_DATA_DB: DirectoryPath = Path(__file__).parents[2] / "data" / "db"
    """Path to the db data sub-folder.""" "data"

    DB_NAME: str = "PRODUCT_RATER"
    """Database name."""

    DB_URI: str = f"sqlite:///{PATH_DATA_DB}/{DB_NAME}.db"

    API_KEY: SecretStr
    """API key for the Amazon Product API."""


config = Config()
