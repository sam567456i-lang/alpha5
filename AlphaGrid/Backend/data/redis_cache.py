"""Redis cache connection and cache manager."""

from __future__ import annotations

from dataclasses import dataclass, field
from inspect import isawaitable
import json
import logging
from typing import Any, Callable

from Backend.foundation import HealthCheckResult, HealthStatus

from .exceptions import DatabaseConnectionError, DatabaseDependencyError
from .settings import RedisSettings

RedisFactory = Callable[..., object]


@dataclass(slots=True)
class RedisConnectionManager:
    """Manage the Redis cache client."""

    settings: RedisSettings
    logger: logging.Logger
    redis_factory: RedisFactory | None = None

    _client: object | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        pass

    @property
    def client(self) -> object:
        """Return the active Redis client."""

        if self._client is None:
            raise DatabaseConnectionError("Redis client is not connected.")
        return self._client

    @property
    def is_connected(self) -> bool:
        """Return whether Redis is connected."""

        return self._client is not None

    def connect(self) -> None:
        """Create the Redis cache client."""

        if self.is_connected:
            return
        redis_factory = self.redis_factory or _load_redis_factory()
        self._client = redis_factory(
            self.settings.redis_url,
            socket_timeout=self.settings.socket_timeout_seconds,
            decode_responses=True,
        )
        self.logger.info(
            "Redis cache connection manager initialized",
            extra={"redis": self.settings.masked_url},
        )

    def health_check(self) -> HealthCheckResult:
        """Run a Redis health check."""

        if not self.is_connected:
            return HealthCheckResult(
                name="database.redis",
                status=HealthStatus.UNKNOWN,
                message="Redis manager is configured but not connected.",
            )
        try:
            healthy = bool(self.client.ping())  # type: ignore[attr-defined]
            return HealthCheckResult(
                name="database.redis",
                status=HealthStatus.HEALTHY if healthy else HealthStatus.UNHEALTHY,
                message="Redis health check completed.",
            )
        except Exception as exc:
            return HealthCheckResult(
                name="database.redis",
                status=HealthStatus.UNHEALTHY,
                message=str(exc),
            )

    async def close(self) -> None:
        """Close the Redis client."""

        if self._client is None:
            return
        close = getattr(self._client, "close", None)
        if callable(close):
            result = close()
            if isawaitable(result):
                await result
        self._client = None
        self.logger.info("Redis cache connection manager closed")


class RedisCacheManager:
    """JSON cache helper for Redis-backed temporary data."""

    def __init__(self, connection_manager: RedisConnectionManager) -> None:
        self._connection_manager = connection_manager

    def get(self, key: str) -> Any:
        """Return a decoded cache value or ``None``."""

        raw_value = self._connection_manager.client.get(key)  # type: ignore[attr-defined]
        if raw_value is None:
            return None
        return json.loads(raw_value)

    def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: int | None = None,
    ) -> None:
        """Set a temporary cache value with a configured TTL."""

        ttl = ttl_seconds or self._connection_manager.settings.default_ttl_seconds
        if ttl <= 0:
            raise DatabaseConnectionError("Redis cache TTL must be greater than zero.")
        encoded = json.dumps(value, default=str, separators=(",", ":"))
        self._connection_manager.client.setex(key, ttl, encoded)  # type: ignore[attr-defined]

    def delete(self, key: str) -> None:
        """Delete a cache key."""

        self._connection_manager.client.delete(key)  # type: ignore[attr-defined]

    def invalidate_prefix(self, prefix: str) -> int:
        """Delete all cache keys matching a prefix and return delete count."""

        pattern = f"{prefix}*"
        client = self._connection_manager.client
        keys = list(client.scan_iter(match=pattern))  # type: ignore[attr-defined]
        if not keys:
            return 0
        return int(client.delete(*keys))  # type: ignore[attr-defined]


def _load_redis_factory() -> RedisFactory:
    try:
        import redis
    except ModuleNotFoundError as exc:
        raise DatabaseDependencyError("redis is required for Redis cache access.") from exc
    return redis.Redis.from_url
