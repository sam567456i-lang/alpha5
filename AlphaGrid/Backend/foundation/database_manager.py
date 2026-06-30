"""Foundation database resource manager.

This module manages externally created database resources without opening
connections or defining schema. Concrete PostgreSQL, DuckDB, and Redis
implementations belong to the Database module.
"""

from __future__ import annotations

from dataclasses import dataclass
from inspect import isawaitable
from typing import Callable

from .exceptions import AlphaGridError
from .health_checker import HealthCheckResult, HealthStatus

CloseCallback = Callable[[], object]
ResourceHealthCheck = Callable[[], object]


@dataclass(frozen=True, slots=True)
class DatabaseResource:
    """Registered database-like resource owned by another module."""

    name: str
    close: CloseCallback
    health_check: ResourceHealthCheck | None = None


class DatabaseManager:
    """Track database resources for health and graceful shutdown."""

    def __init__(self) -> None:
        self._resources: dict[str, DatabaseResource] = {}

    def register_resource(
        self,
        name: str,
        close: CloseCallback,
        health_check: ResourceHealthCheck | None = None,
    ) -> None:
        """Register a database resource close hook and optional health check."""

        if name.strip() == "":
            raise AlphaGridError("Database resource name must not be empty.")
        if name in self._resources:
            raise AlphaGridError(f"Database resource already registered: {name}")
        self._resources[name] = DatabaseResource(
            name=name,
            close=close,
            health_check=health_check,
        )

    def registered_names(self) -> tuple[str, ...]:
        """Return registered database resource names."""

        return tuple(sorted(self._resources))

    async def health(self) -> tuple[HealthCheckResult, ...]:
        """Run registered database health checks."""

        results: list[HealthCheckResult] = []
        for resource in self._resources.values():
            if resource.health_check is None:
                results.append(
                    HealthCheckResult(
                        name=resource.name,
                        status=HealthStatus.UNKNOWN,
                        message="No health check registered.",
                    )
                )
                continue
            try:
                checked = resource.health_check()
                if isawaitable(checked):
                    checked = await checked
                if isinstance(checked, HealthCheckResult):
                    results.append(checked)
                else:
                    healthy = bool(checked)
                    results.append(
                        HealthCheckResult(
                            name=resource.name,
                            status=HealthStatus.HEALTHY
                            if healthy
                            else HealthStatus.UNHEALTHY,
                            message="Resource health check completed.",
                        )
                    )
            except Exception as exc:
                results.append(
                    HealthCheckResult(
                        name=resource.name,
                        status=HealthStatus.UNHEALTHY,
                        message=str(exc),
                    )
                )
        return tuple(results)

    async def close_all(self) -> None:
        """Close all registered database resources."""

        errors: list[BaseException] = []
        for resource in reversed(tuple(self._resources.values())):
            try:
                result = resource.close()
                if isawaitable(result):
                    await result
            except BaseException as exc:
                errors.append(exc)
        if errors:
            raise AlphaGridError(
                f"{len(errors)} database resource(s) failed to close."
            ) from errors[0]
