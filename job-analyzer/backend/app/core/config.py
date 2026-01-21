import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="job-analyzer", validation_alias="APP_NAME")
    env: str = Field(default="dev", validation_alias="ENV")

    # Use a file-based SQLite DB by default (creates ./dev.db).
    database_url: str = Field(default="sqlite:///./dev.db", validation_alias="DATABASE_URL")

    openai_api_key: str | None = Field(default=None, validation_alias="OPENAI_API_KEY")


settings = Settings()

# If the key is provided via `.env` (pydantic-settings), expose it as a real
# environment variable too (e.g., for SDKs that rely on `OPENAI_API_KEY`).
if settings.openai_api_key and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key

