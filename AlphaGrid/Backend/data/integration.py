"""Database module integration with Foundation services."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from Backend.foundation import ApplicationContext

from .duckdb_manager import DuckDBConnectionManager
from .migration import MigrationManager
from .postgres import PostgreSQLConnectionManager
from .redis_cache import RedisCacheManager, RedisConnectionManager
from .settings import DatabaseSettings, load_database_settings
from .transaction_manager import TransactionManager


@dataclass(frozen=True, slots=True)
class DatabaseModule:
    """Composed database infrastructure services."""

    settings: DatabaseSettings
    postgresql: PostgreSQLConnectionManager
    duckdb: DuckDBConnectionManager
    redis: RedisConnectionManager
    cache: RedisCacheManager
    migrations: MigrationManager


def create_database_module(
    context: ApplicationContext,
    project_root: str | Path,
    environ: Mapping[str, str],
    settings: DatabaseSettings | None = None,
) -> DatabaseModule:
    """Create database infrastructure and register it with Foundation."""

    database_settings = settings or load_database_settings(environ, project_root)
    postgresql = PostgreSQLConnectionManager(
        settings=database_settings.postgresql,
        logger=context.logger,
    )
    duckdb = DuckDBConnectionManager(
        settings=database_settings.duckdb,
        logger=context.logger,
    )
    redis = RedisConnectionManager(
        settings=database_settings.redis,
        logger=context.logger,
    )
    cache = RedisCacheManager(redis)
    migrations = MigrationManager(
        settings=database_settings.migrations,
        database_url=database_settings.postgresql.sqlalchemy_url,
    )
    module = DatabaseModule(
        settings=database_settings,
        postgresql=postgresql,
        duckdb=duckdb,
        redis=redis,
        cache=cache,
        migrations=migrations,
    )

    _register_database_services(context, module)
    return module


def _register_database_services(
    context: ApplicationContext,
    module: DatabaseModule,
) -> None:
    context.container.register_instance("database.settings", module.settings)
    context.container.register_instance("database.postgresql", module.postgresql)
    context.container.register_instance("database.duckdb", module.duckdb)
    context.container.register_instance("database.redis", module.redis)
    context.container.register_instance("database.cache", module.cache)
    context.container.register_instance("database.migrations", module.migrations)
    context.container.register_factory(
        "database.transaction_manager",
        lambda container: TransactionManager(
            container.resolve(  # type: ignore
                "database.postgresql",
                PostgreSQLConnectionManager,
            ).session_factory
        ),
    )

    context.database_manager.register_resource(
        "postgresql",
        close=module.postgresql.close,
        health_check=module.postgresql.health_check,
    )
    context.database_manager.register_resource(
        "duckdb",
        close=module.duckdb.close,
        health_check=module.duckdb.health_check,
    )
    context.database_manager.register_resource(
        "redis",
        close=module.redis.close,
        health_check=module.redis.health_check,
    )

    context.health_checker.register(
        "database.configuration",
        lambda: True,
    )
    context.health_checker.register(
        "database.postgresql",
        module.postgresql.health_check,
    )
    context.health_checker.register(
        "database.duckdb",
        module.duckdb.health_check,
    )
    context.health_checker.register(
        "database.redis",
        module.redis.health_check,
    )
