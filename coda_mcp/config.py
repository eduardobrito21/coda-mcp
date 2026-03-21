from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    coda_api_key: SecretStr
    coda_base_url: str = "https://coda.io/apis/v1"


settings = Settings(**{})  # pyright: ignore[reportUnknownArgumentType]
