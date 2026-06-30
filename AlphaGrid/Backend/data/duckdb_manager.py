"""DuckDB analytical connection management."""

from __future__ import annotations

from dataclasses import dataclass, field
import logging
from pathlib import Path
from typing import Any, Callable, Sequence

from Backend.foundation import HealthCheckResult, HealthStatus

from .exceptions import (
    DatabaseConnectionError,
    DatabaseDependencyError,
    DatabaseWritePolicyError,
)
from .settings import DuckDBSettings

DuckDBConnect = Callable[..., object]


@dataclass(slots=True)
class DuckDBConnectionManager:
    """Manage the read-only DuckDB analytics connection."""

    settings: DuckDBSettings
    logger: logging.Logger
    connector: DuckDBConnect | None = None

    _connection: object | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        pass

    @property
    def connection(self) -> object:
        """Return the active DuckDB connection."""

        if self._connection is None:
            raise DatabaseConnectionError("DuckDB connection is not open.")
        return self._connection

    @property
    def is_connected(self) -> bool:
        """Return whether DuckDB is connected."""

        return self._connection is not None

    def connect(self) -> None:
        """Open the DuckDB analytics connection."""

        if self.is_connected:
            return
        if self.settings.read_only and not Path(self.settings.path).exists():
            raise DatabaseConnectionError(
                "DuckDB read-only connection requires an existing database file."
            )
        connector = self.connector or _load_duckdb_connect()
        self._connection = connector(
            database=str(self.settings.path),
            read_only=self.settings.read_only,
        )
        self.logger.info(
            "DuckDB analytics connection opened",
            extra={"duckdb_path": str(self.settings.path), "read_only": True},
        )

    def execute_read(
        self,
        statement: str,
        parameters: Sequence[Any] | None = None,
    ) -> object:
        """Execute a read-only analytical statement."""

        if _is_mutating_statement(statement):
            raise DatabaseWritePolicyError("DuckDB application writes are forbidden.")
        cursor = self.connection.execute(statement, parameters or [])  # type: ignore[attr-defined]
        return cursor.fetchall()

    def health_check(self) -> HealthCheckResult:
        """Run a DuckDB health check."""

        if not self.is_connected:
            return HealthCheckResult(
                name="database.duckdb",
                status=HealthStatus.UNKNOWN,
                message="DuckDB manager is configured but not connected.",
            )
        try:
            self.execute_read("SELECT 1")
            return HealthCheckResult(
                name="database.duckdb",
                status=HealthStatus.HEALTHY,
                message="DuckDB health check passed.",
            )
        except Exception as exc:
            return HealthCheckResult(
                name="database.duckdb",
                status=HealthStatus.UNHEALTHY,
                message=str(exc),
            )

    async def close(self) -> None:
        """Close the DuckDB connection."""

        if self._connection is None:
            return
        self._connection.close()  # type: ignore[attr-defined]
        self._connection = None
        self.logger.info("DuckDB analytics connection closed")


def _load_duckdb_connect() -> DuckDBConnect:
    try:
        import duckdb
    except ModuleNotFoundError as exc:
        raise DatabaseDependencyError("duckdb is required for DuckDB access.") from exc
    return duckdb.connect


def _is_mutating_statement(statement: str) -> bool:
    stripped = statement.lstrip().lower()
    mutating_prefixes = (
        "alter ",
        "attach ",
        "create ",
        "delete ",
        "drop ",
        "insert ",
        "merge ",
        "replace ",
        "truncate ",
        "update ",
    )
    return stripped.startswith(mutating_prefixes)
