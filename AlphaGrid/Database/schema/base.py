"""SQLAlchemy migration base metadata.

No business tables are declared in the Database module.
"""

from __future__ import annotations

try:
    from sqlalchemy.orm import DeclarativeBase
except ModuleNotFoundError:
    Base = None
    target_metadata = None
else:

    class Base(DeclarativeBase):
        """Base class for future approved ORM models."""

    target_metadata = Base.metadata
