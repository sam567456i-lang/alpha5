"""AlphaGrid Database module public API."""

from .duckdb_manager import DuckDBConnectionManager
from .exceptions import (
    DatabaseConfigurationError,
    DatabaseConnectionError,
    DatabaseDependencyError,
    DatabaseError,
    DatabaseMigrationError,
    DatabaseTransactionError,
    DatabaseWritePolicyError,
    RepositoryError,
)
from .integration import DatabaseModule, create_database_module
from .migration import MigrationManager, migration_base_path
from .postgres import PostgreSQLConnectionManager
from .redis_cache import RedisCacheManager, RedisConnectionManager
from .repository import BaseRepository, CRUDRepository
from .settings import (
    DatabaseSettings,
    DuckDBSettings,
    MigrationSettings,
    PostgreSQLSettings,
    RedisSettings,
    load_database_settings,
)
from .transaction_manager import TransactionManager

__all__ = [
    "BaseRepository",
    "CRUDRepository",
    "DatabaseConfigurationError",
    "DatabaseConnectionError",
    "DatabaseDependencyError",
    "DatabaseError",
    "DatabaseMigrationError",
    "DatabaseModule",
    "DatabaseSettings",
    "DatabaseTransactionError",
    "DatabaseWritePolicyError",
    "DuckDBConnectionManager",
    "DuckDBSettings",
    "MigrationManager",
    "MigrationSettings",
    "PostgreSQLConnectionManager",
    "PostgreSQLSettings",
    "RedisCacheManager",
    "RedisConnectionManager",
    "RedisSettings",
    "RepositoryError",
    "TransactionManager",
    "create_database_module",
    "load_database_settings",
    "migration_base_path",
]
