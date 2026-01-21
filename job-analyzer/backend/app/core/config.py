from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Use a file-based SQLite DB by default (creates ./app.db).
    database_url: str = "sqlite:///./app.db"


settings = Settings()

