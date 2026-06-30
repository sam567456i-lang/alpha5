"""Database settings and environment validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping
from urllib.parse import quote_plus

from .exceptions import DatabaseConfigurationError


@dataclass(frozen=True, slots=True)
class PostgreSQLSettings:
    """PostgreSQL connection and pool settings."""

    host: str
    port: int
    database: str
    user: str
    password: str
    pool_size: int
    max_overflow: int
    pool_timeout_seconds: float
    echo_sql: bool

    @property
    def sqlalchemy_url(self) -> str:
        """Return a SQLAlchemy PostgreSQL URL without logging it."""

        user = quote_plus(self.user)
        password = quote_plus(self.password)
        host = self.host
        database = quote_plus(self.database)
        return f"postgresql+psycopg://{user}:{password}@{host}:{self.port}/{database}"

    @property
    def masked_url(self) -> str:
        """Return a redacted PostgreSQL URL for diagnostics."""

        user = quote_plus(self.user)
        host = self.host
        database = quote_plus(self.database)
        return f"postgresql+psycopg://{user}:[REDACTED]@{host}:{self.port}/{database}"


@dataclass(frozen=True, slots=True)
class DuckDBSettings:
    """DuckDB analytical connection settings."""

    path: Path
    read_only: bool


@dataclass(frozen=True, slots=True)
class RedisSettings:
    """Redis cache connection settings."""

    host: str
    port: int
    database: int
    password: str
    default_ttl_seconds: int
    socket_timeout_seconds: float

    @property
    def redis_url(self) -> str:
        """Return a Redis URL without logging it."""

        auth = f":{quote_plus(self.password)}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.database}"

    @property
    def masked_url(self) -> str:
        """Return a redacted Redis URL for diagnostics."""

        auth = ":[REDACTED]@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.database}"


@dataclass(frozen=True, slots=True)
class MigrationSettings:
    """Alembic migration file locations."""

    config_path: Path
    script_location: Path


@dataclass(frozen=True, slots=True)
class DatabaseSettings:
    """Validated database module settings."""

    postgresql: PostgreSQLSettings
    duckdb: DuckDBSettings
    redis: RedisSettings
    migrations: MigrationSettings

    def as_safe_dict(self) -> dict[str, object]:
        """Return settings with secrets redacted."""

        return {
            "postgresql": {
                "url": self.postgresql.masked_url,
                "pool_size": self.postgresql.pool_size,
                "max_overflow": self.postgresql.max_overflow,
                "pool_timeout_seconds": self.postgresql.pool_timeout_seconds,
                "echo_sql": self.postgresql.echo_sql,
            },
            "duckdb": {
                "path": str(self.duckdb.path),
                "read_only": self.duckdb.read_only,
            },
            "redis": {
                "url": self.redis.masked_url,
                "default_ttl_seconds": self.redis.default_ttl_seconds,
                "socket_timeout_seconds": self.redis.socket_timeout_seconds,
            },
            "migrations": {
                "config_path": str(self.migrations.config_path),
                "script_location": str(self.migrations.script_location),
            },
        }


def load_database_settings(
    environ: Mapping[str, str],
    project_root: str | Path,
) -> DatabaseSettings:
    """Load and validate database settings from environment values."""

    root = Path(project_root)
    database_root = root / "Database"
    return DatabaseSettings(
        postgresql=PostgreSQLSettings(
            host=_read_string(environ, "POSTGRES_HOST", "localhost"),
            port=_read_int(environ, "POSTGRES_PORT", 5432),
            database=_read_string(environ, "POSTGRES_DB", "alphagrid"),
            user=_read_string(environ, "POSTGRES_USER", "alphagrid"),
            password=_read_string(environ, "POSTGRES_PASSWORD", ""),
            pool_size=_read_int(environ, "POSTGRES_POOL_SIZE", 5),
            max_overflow=_read_int(environ, "POSTGRES_MAX_OVERFLOW", 10),
            pool_timeout_seconds=_read_float(
                environ,
                "POSTGRES_POOL_TIMEOUT_SECONDS",
                30.0,
            ),
            echo_sql=_read_bool(environ, "POSTGRES_ECHO_SQL", False),
        ),
        duckdb=DuckDBSettings(
            path=_read_path(environ, "DUCKDB_PATH", root / "Database" / "alphagrid.duckdb"),
            read_only=_read_bool(environ, "DUCKDB_READ_ONLY", True),
        ),
        redis=RedisSettings(
            host=_read_string(environ, "REDIS_HOST", "localhost"),
            port=_read_int(environ, "REDIS_PORT", 6379),
            database=_read_int(environ, "REDIS_DB", 0),
            password=_read_string(environ, "REDIS_PASSWORD", ""),
            default_ttl_seconds=_read_int(environ, "REDIS_DEFAULT_TTL_SECONDS", 300),
            socket_timeout_seconds=_read_float(
                environ,
                "REDIS_SOCKET_TIMEOUT_SECONDS",
                5.0,
            ),
        ),
        migrations=MigrationSettings(
            config_path=_read_path(
                environ,
                "ALEMBIC_CONFIG_PATH",
                database_root / "alembic.ini",
            ),
            script_location=_read_path(
                environ,
                "ALEMBIC_SCRIPT_LOCATION",
                database_root / "migrations",
            ),
        ),
    )


def _read_string(values: Mapping[str, str], key: str, default: str) -> str:
    value = values.get(key, default)
    if value is None:
        return default
    return str(value).strip()


def _read_int(values: Mapping[str, str], key: str, default: int) -> int:
    raw_value = _read_string(values, key, str(default))
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise DatabaseConfigurationError(f"{key} must be an integer.") from exc
    if value < 0:
        raise DatabaseConfigurationError(f"{key} must be zero or greater.")
    return value


def _read_float(values: Mapping[str, str], key: str, default: float) -> float:
    raw_value = _read_string(values, key, str(default))
    try:
        value = float(raw_value)
    except ValueError as exc:
        raise DatabaseConfigurationError(f"{key} must be a number.") from exc
    if value <= 0:
        raise DatabaseConfigurationError(f"{key} must be greater than zero.")
    return value


def _read_bool(values: Mapping[str, str], key: str, default: bool) -> bool:
    raw_value = _read_string(values, key, str(default)).lower()
    if raw_value in {"1", "true", "yes", "on"}:
        return True
    if raw_value in {"0", "false", "no", "off"}:
        return False
    raise DatabaseConfigurationError(f"{key} must be a boolean value.")


def _read_path(values: Mapping[str, str], key: str, default: Path) -> Path:
    raw_value = _read_string(values, key, str(default))
    return Path(raw_value).expanduser()
