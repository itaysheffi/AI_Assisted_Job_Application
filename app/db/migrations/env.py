from __future__ import annotations

from logging.config import fileConfig
from pathlib import Path
import sys

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

# Ensure we import the *real* backend `app` package (job-analyzer/backend/app),
# not this repo-root `app/` migrations folder.
_REPO_ROOT = Path(__file__).resolve().parents[3]
_BACKEND_DIR = _REPO_ROOT / "job-analyzer" / "backend"
sys.path.insert(0, str(_BACKEND_DIR))

from app.core.config import settings  # noqa: E402
from app.db.session import Base  # noqa: E402


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Always use DATABASE_URL from our app settings (no alembic.ini hardcoding).
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Autogenerate needs a MetaData to compare against.
target_metadata = Base.metadata


def _is_sqlite(url: str) -> bool:
    return url.strip().lower().startswith("sqlite")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        render_as_batch=_is_sqlite(url),
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    url = config.get_main_option("sqlalchemy.url")
    connect_args = {"check_same_thread": False} if _is_sqlite(url) else {}

    engine = create_engine(url, poolclass=NullPool, connect_args=connect_args)

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            render_as_batch=_is_sqlite(url),
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
