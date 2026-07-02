"""PostgreSQL connection management."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from inspect import isawaitable
import logging
from typing import Callable, Iterator

from Backend.foundation import HealthCheckResult, HealthStatus

from .exceptions import DatabaseConnectionError, DatabaseDependencyError
from .settings import PostgreSQLSettings

EngineFactory = Callable[..., object]
SessionMakerFactory = Callable[..., Callable[[], object]]
TextFactory = Callable[[str], object]


@dataclass(slots=True)
class PostgreSQLConnectionManager:
    """Manage PostgreSQL engine, pool, and session factory."""

    settings: PostgreSQLSettings
    logger: logging.Logger
    engine_factory: EngineFactory | None = None
    sessionmaker_factory: SessionMakerFactory | None = None
    text_factory: TextFactory | None = None

    _engine: object | None = field(default=None, init=False)
    _session_factory: Callable[[], object] | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        pass

    @property
    def engine(self) -> object:
        """Return the initialized SQLAlchemy engine."""

        if self._engine is None:
            raise DatabaseConnectionError("PostgreSQL engine is not connected.")
        return self._engine

    @property
    def session_factory(self) -> Callable[[], object]:
        """Return the initialized SQLAlchemy session factory."""

        if self._session_factory is None:
            raise DatabaseConnectionError("PostgreSQL session factory is not ready.")
        return self._session_factory

    @property
    def is_connected(self) -> bool:
        """Return whether the engine and session factory are initialized."""

        return self._engine is not None and self._session_factory is not None

    def connect(self) -> None:
        """Create the PostgreSQL engine and session factory."""

        if self.is_connected:
            return
        engine_factory = self.engine_factory or _load_create_engine()
        sessionmaker_factory = self.sessionmaker_factory or _load_sessionmaker()
        self._engine = engine_factory(
            self.settings.sqlalchemy_url,
            pool_size=self.settings.pool_size,
            max_overflow=self.settings.max_overflow,
            pool_timeout=self.settings.pool_timeout_seconds,
            echo=self.settings.echo_sql,
            future=True,
        )
        self._session_factory = sessionmaker_factory(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
        self.logger.info(
            "PostgreSQL connection manager initialized",
            extra={"database": self.settings.masked_url},
        )

    @contextmanager
    def session_scope(self) -> Iterator[object]:
        """Provide a transactional PostgreSQL session scope."""

        session = self.session_factory()
        try:
            yield session
            session.commit()  # type: ignore
        except Exception:
            session.rollback()  # type: ignore
            raise
        finally:
            session.close()  # type: ignore

    def health_check(self) -> HealthCheckResult:
        """Run a PostgreSQL health check."""

        if not self.is_connected:
            return HealthCheckResult(
                name="database.postgresql",
                status=HealthStatus.UNKNOWN,
                message="PostgreSQL manager is configured but not connected.",
            )
        try:
            text = self.text_factory or _load_text()
            with self.engine.connect() as connection:  # type: ignore[attr-defined]
                connection.execute(text("SELECT 1"))
            return HealthCheckResult(
                name="database.postgresql",
                status=HealthStatus.HEALTHY,
                message="PostgreSQL health check passed.",
            )
        except Exception as exc:
            return HealthCheckResult(
                name="database.postgresql",
                status=HealthStatus.UNHEALTHY,
                message=str(exc),
            )

    async def close(self) -> None:
        """Dispose of the PostgreSQL engine."""

        if self._engine is None:
            return
        dispose = getattr(self._engine, "dispose")
        result = dispose()
        if isawaitable(result):
            await result
        self._engine = None
        self._session_factory = None
        self.logger.info("PostgreSQL connection manager closed")


def _load_create_engine() -> EngineFactory:
    try:
        from sqlalchemy import create_engine
    except ModuleNotFoundError as exc:
        raise DatabaseDependencyError(
            "SQLAlchemy is required for PostgreSQL connections."
        ) from exc
    return create_engine  # type: ignore


def _load_sessionmaker() -> SessionMakerFactory:
    try:
        from sqlalchemy.orm import sessionmaker
    except ModuleNotFoundError as exc:
        raise DatabaseDependencyError(
            "SQLAlchemy is required for PostgreSQL session factories."
        ) from exc
    return sessionmaker  # type: ignore


def _load_text() -> TextFactory:
    try:
        from sqlalchemy import text
    except ModuleNotFoundError as exc:
        raise DatabaseDependencyError(
            "SQLAlchemy is required for PostgreSQL health checks."
        ) from exc
    return text  # type: ignore
