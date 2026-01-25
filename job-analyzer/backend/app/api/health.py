"""Compatibility shim.

Health routes live under `app.api.routes.health`. This file re-exports the router so
older imports (`from app.api.health import router`) keep working.
"""

from app.api.routes.health import router  # noqa: F401

