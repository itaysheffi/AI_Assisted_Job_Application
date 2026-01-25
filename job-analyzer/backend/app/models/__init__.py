"""
SQLAlchemy model package.

Alembic's autogenerate only "sees" models that are imported at runtime.
Import all model modules here (e.g. `from .user import User`) so that
`Base.metadata` is populated when `alembic revision --autogenerate` runs.
"""

from app.models.user import User  # noqa: F401


