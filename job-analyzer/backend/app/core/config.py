import os


def _parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "t", "yes", "y", "on"}


class Config:
    """Runtime configuration loaded from environment variables.

    Note: `.env` is loaded in `app/main.py` using python-dotenv.
    """

    def __init__(self) -> None:
        self.env: str = os.getenv("ENV", "development")
        self.debug: bool = _parse_bool(os.getenv("DEBUG"), default=False)

        openai_api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
        if not openai_api_key:
            raise RuntimeError(
                "Missing required environment variable OPENAI_API_KEY. "
                "Set it in your environment (or in backend/.env) and restart the server."
            )

        self.openai_api_key: str = openai_api_key


settings = Config()

