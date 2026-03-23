from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    coda_api_key: SecretStr | None = None
    coda_base_url: str = "https://coda.io/apis/v1"

    #: If False, HTTP MCP traffic never uses ``CODA_API_KEY`` from the server env — callers must send
    #: ``X-Coda-Api-Key`` or ``?coda_api_key=`` so each user uses their own Coda account (public multi-tenant).
    coda_mcp_http_allow_env_api_key: bool = Field(default=False)


settings = Settings(**{})  # pyright: ignore[reportUnknownArgumentType]
