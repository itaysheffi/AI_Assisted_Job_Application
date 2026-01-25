from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Final
from urllib.parse import urlparse

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_DIR: Final[Path] = Path(__file__).resolve().parents[2]
_DOTENV_FILES: Final[tuple[Path, ...]] = (
    _BACKEND_DIR / ".env",
    _BACKEND_DIR / ".env.local",
)
_STRICT_ENVS: Final[set[str]] = {"production", "prod", "staging"}


class Settings(BaseSettings):
    """Production-grade settings loaded from `.env` + environment variables.

    - `.env` files are optional and intended for local dev/test.
    - In production, required settings are validated and the app fails fast if missing.
    """

    model_config = SettingsConfigDict(
        env_file=_DOTENV_FILES,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Required by the prompt
    ENV: str = Field(default="development")
    DATABASE_URL: str = Field(default="sqlite:///./dev.db")
    SECRET_KEY: str | None = Field(default=None)

    # Existing / optional (kept for compatibility)
    DEBUG: bool = Field(default=False)
    OPENAI_API_KEY: str | None = Field(default=None)

    @field_validator("ENV", mode="before")
    @classmethod
    def _normalize_env(cls, v: object) -> str:
        value = ("" if v is None else str(v)).strip().lower()
        return value or "development"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def _normalize_database_url(cls, v: object) -> str:
        value = ("" if v is None else str(v)).strip()
        return value or "sqlite:///./dev.db"

    @field_validator("SECRET_KEY", "OPENAI_API_KEY", mode="before")
    @classmethod
    def _normalize_optional_secret(cls, v: object) -> str | None:
        value = ("" if v is None else str(v)).strip()
        return value or None

    @model_validator(mode="after")
    def _validate_environment_requirements(self) -> "Settings":
        # SECRET_KEY is required only for production/staging.
        if self.ENV in _STRICT_ENVS:
            if not self.SECRET_KEY:
                raise ValueError("SECRET_KEY must be set when ENV is production/staging.")
        else:
            # Dev/test convenience: ensure SECRET_KEY exists (still never log it).
            if not self.SECRET_KEY:
                self.SECRET_KEY = "dev-insecure-secret-key"

        return self

    # Backwards-compatible aliases (existing code uses snake_case)
    @property
    def env(self) -> str:  # pragma: no cover
        return self.ENV

    @property
    def debug(self) -> bool:  # pragma: no cover
        return self.DEBUG

    @property
    def openai_api_key(self) -> str | None:  # pragma: no cover
        return self.OPENAI_API_KEY

    def safe_database_target(self) -> str:
        """A log-safe representation of the configured DB target (no secrets)."""
        parsed = urlparse(self.DATABASE_URL)

        # For sqlite, the URL doesn't contain credentials; return scheme + path-ish.
        if parsed.scheme == "sqlite":
            return "sqlite"

        host = parsed.hostname or "unknown-host"
        port = f":{parsed.port}" if parsed.port else ""
        db = (parsed.path or "").lstrip("/") or "unknown-db"
        return f"{parsed.scheme}://{host}{port}/{db}"

    def dotenv_file_status(self) -> dict[str, bool]:
        """Which `.env` files are considered, and whether they exist."""
        return {str(p): p.exists() for p in _DOTENV_FILES}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

