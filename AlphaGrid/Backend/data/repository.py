"""Generic repository interfaces for future business repositories."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar, runtime_checkable

from .exceptions import RepositoryError

EntityT = TypeVar("EntityT")
IdentifierT = TypeVar("IdentifierT")


@runtime_checkable
class CRUDRepository(Protocol[EntityT, IdentifierT]):
    """CRUD interface that future business repositories must implement."""

    def add(self, entity: EntityT) -> EntityT:
        """Persist an entity."""

    def get(self, identifier: IdentifierT) -> EntityT | None:
        """Return an entity by identifier."""

    def list(self, *, limit: int = 100, offset: int = 0) -> tuple[EntityT, ...]:
        """Return a paginated entity list."""

    def delete(self, entity: EntityT) -> None:
        """Delete an entity."""


@dataclass(slots=True)
class BaseRepository(Generic[EntityT, IdentifierT]):
    """SQLAlchemy-backed generic repository base class.

    This class contains no business query logic and creates no tables.
    """

    session: object
    entity_type: type[EntityT]

    def add(self, entity: EntityT) -> EntityT:
        """Persist an entity in the active session."""

        try:
            self.session.add(entity)  # type: ignore[attr-defined]
            return entity
        except Exception as exc:
            raise RepositoryError("Could not add entity.") from exc

    def get(self, identifier: IdentifierT) -> EntityT | None:
        """Return an entity by primary key."""

        try:
            return self.session.get(self.entity_type, identifier)  # type: ignore[attr-defined]
        except Exception as exc:
            raise RepositoryError("Could not get entity.") from exc

    def list(self, *, limit: int = 100, offset: int = 0) -> tuple[EntityT, ...]:
        """Return a paginated entity list."""

        if limit <= 0:
            raise RepositoryError("limit must be greater than zero.")
        if offset < 0:
            raise RepositoryError("offset must be zero or greater.")
        try:
            statement = _build_select(self.entity_type, limit, offset)
            result = self.session.execute(statement)  # type: ignore[attr-defined]
            return tuple(result.scalars().all())
        except Exception as exc:
            raise RepositoryError("Could not list entities.") from exc

    def delete(self, entity: EntityT) -> None:
        """Delete an entity from the active session."""

        try:
            self.session.delete(entity)  # type: ignore[attr-defined]
        except Exception as exc:
            raise RepositoryError("Could not delete entity.") from exc


def _build_select(entity_type: type[EntityT], limit: int, offset: int) -> object:
    try:
        from sqlalchemy import select
    except ModuleNotFoundError as exc:
        raise RepositoryError("SQLAlchemy is required for repository listing.") from exc
    return select(entity_type).limit(limit).offset(offset)
