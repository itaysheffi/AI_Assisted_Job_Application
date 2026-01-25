from __future__ import annotations

from logging.config import fileConfig
from pathlib import Path
import sys

from alembic import context
from sqlalchemy import create_engine, pool

# --- Ensure `import app...` works no matter where Alembic is run from ---
_BACKEND_DIR = Path(__file__).resolve().parents[1]  # job-analyzer/backend
sys.path.insert(0, str(_BACKEND_DIR))

from app.core.config import settings  # noqa: E402
from app.db.session import Base  # noqa: E402


def _import_models() -> None:
    """Import model modules so Base.metadata is populated for autogenerate.

    Put your SQLAlchemy models under `app/models/` and import them in
    `app/models/__init__.py`. This function makes sure that package is imported.
    """

    # `app.models` may not exist yet in early scaffolding stages.
    try:
        import app.models  # noqa: F401
    except ModuleNotFoundError:
        return


# this is the Alembic Config object, which provides access to the values within
# the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Dynamically set sqlalchemy.url from our application settings (no hardcoding).
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Make sure models are imported before we expose metadata for autogenerate.
_import_models()

# Alembic autogenerate will compare against this metadata.
target_metadata = Base.metadata


def _is_sqlite(url: str) -> bool:
    return url.strip().lower().startswith("sqlite")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (no DB connection)."""

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
    """Run migrations in 'online' mode (with DB connection)."""

    url = config.get_main_option("sqlalchemy.url")
    connect_args = {"check_same_thread": False} if _is_sqlite(url) else {}

    engine = create_engine(url, poolclass=pool.NullPool, connect_args=connect_args)

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
