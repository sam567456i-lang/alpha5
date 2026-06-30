"""Health check orchestration for foundation services."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from inspect import isawaitable
from time import perf_counter
from typing import Any, Callable, Mapping

from .exceptions import HealthCheckError

HealthCheck = Callable[[], object]


class HealthStatus(StrEnum):
    """Supported health states."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class HealthCheckResult:
    """Result returned by a health check."""

    name: str
    status: HealthStatus
    message: str
    checked_at: str = field(
        default_factory=lambda: datetime.now(tz=timezone.utc).isoformat()
    )
    latency_ms: float = 0.0
    details: Mapping[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        """Return a serializable health result."""

        return {
            "name": self.name,
            "status": self.status.value,
            "message": self.message,
            "checked_at": self.checked_at,
            "latency_ms": self.latency_ms,
            "details": dict(self.details),
        }


class HealthChecker:
    """Registry and executor for module health checks."""

    def __init__(self, timeout_seconds: float = 5.0) -> None:
        if timeout_seconds <= 0:
            raise HealthCheckError("timeout_seconds must be greater than zero.")
        self._timeout_seconds = timeout_seconds
        self._checks: dict[str, HealthCheck] = {}

    def register(self, name: str, check: HealthCheck) -> None:
        """Register a health check by name."""

        if name.strip() == "":
            raise HealthCheckError("Health check name must not be empty.")
        if not callable(check):
            raise HealthCheckError("Health check must be callable.")
        if name in self._checks:
            raise HealthCheckError(f"Health check already registered: {name}")
        self._checks[name] = check

    def registered_names(self) -> tuple[str, ...]:
        """Return registered health check names."""

        return tuple(sorted(self._checks))

    async def run(self, name: str) -> HealthCheckResult:
        """Run one registered health check."""

        check = self._checks.get(name)
        if check is None:
            raise HealthCheckError(f"Health check is not registered: {name}")
        started = perf_counter()
        try:
            raw_result = check()
            if isawaitable(raw_result):
                raw_result = await asyncio.wait_for(
                    raw_result,
                    timeout=self._timeout_seconds,
                )
            latency_ms = (perf_counter() - started) * 1000
            return self._normalize_result(name, raw_result, latency_ms)
        except Exception as exc:
            latency_ms = (perf_counter() - started) * 1000
            return HealthCheckResult(
                name=name,
                status=HealthStatus.UNHEALTHY,
                message=str(exc),
                latency_ms=latency_ms,
            )

    async def run_all(self) -> tuple[HealthCheckResult, ...]:
        """Run all registered health checks."""

        return tuple([await self.run(name) for name in self.registered_names()])

    def overall_status(
        self,
        results: tuple[HealthCheckResult, ...],
    ) -> HealthStatus:
        """Calculate overall status from individual health check results."""

        statuses = {result.status for result in results}
        if HealthStatus.UNHEALTHY in statuses:
            return HealthStatus.UNHEALTHY
        if HealthStatus.DEGRADED in statuses:
            return HealthStatus.DEGRADED
        if HealthStatus.UNKNOWN in statuses:
            return HealthStatus.UNKNOWN
        return HealthStatus.HEALTHY

    @staticmethod
    def _normalize_result(
        name: str,
        raw_result: object,
        latency_ms: float,
    ) -> HealthCheckResult:
        if isinstance(raw_result, HealthCheckResult):
            return HealthCheckResult(
                name=raw_result.name,
                status=raw_result.status,
                message=raw_result.message,
                checked_at=raw_result.checked_at,
                latency_ms=latency_ms,
                details=raw_result.details,
            )
        if isinstance(raw_result, bool):
            return HealthCheckResult(
                name=name,
                status=HealthStatus.HEALTHY
                if raw_result
                else HealthStatus.UNHEALTHY,
                message="Health check returned a boolean status.",
                latency_ms=latency_ms,
            )
        raise HealthCheckError(
            "Health checks must return bool or HealthCheckResult instances."
        )
