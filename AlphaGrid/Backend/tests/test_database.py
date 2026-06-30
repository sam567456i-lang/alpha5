"""Tests for the Database module."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from Backend.data import (
    DatabaseConnectionError,
    DatabaseDependencyError,
    DatabaseMigrationError,
    DatabaseWritePolicyError,
    DuckDBConnectionManager,
    PostgreSQLConnectionManager,
    RedisCacheManager,
    RedisConnectionManager,
    TransactionManager,
    create_database_module,
    load_database_settings,
)
from Backend.foundation import HealthStatus, create_application_context


class DatabaseSettingsTests(unittest.TestCase):
    def test_loads_valid_database_settings(self) -> None:
        settings = load_database_settings(
            environ={
                "POSTGRES_HOST": "db",
                "POSTGRES_PORT": "5433",
                "POSTGRES_DB": "alphagrid_test",
                "POSTGRES_USER": "user",
                "POSTGRES_PASSWORD": "secret",
                "DUCKDB_PATH": "analytics.duckdb",
                "REDIS_HOST": "cache",
                "REDIS_PORT": "6380",
                "REDIS_PASSWORD": "redis-secret",
            },
            project_root=Path("."),
        )

        self.assertEqual(settings.postgresql.host, "db")
        self.assertEqual(settings.postgresql.port, 5433)
        self.assertIn("[REDACTED]", settings.postgresql.masked_url)
        self.assertEqual(settings.duckdb.path, Path("analytics.duckdb"))
        self.assertEqual(settings.redis.port, 6380)
        self.assertIn("[REDACTED]", settings.redis.masked_url)


class PostgreSQLConnectionManagerTests(unittest.TestCase):
    def test_connects_with_injected_factories_and_closes(self) -> None:
        settings = load_database_settings({}, Path(".")).postgresql
        engine = _FakeEngine()

        def engine_factory(*_args: object, **_kwargs: object) -> _FakeEngine:
            return engine

        def sessionmaker_factory(**_kwargs: object) -> type[_FakeSession]:
            return _FakeSession

        manager = PostgreSQLConnectionManager(
            settings=settings,
            logger=_NullLogger(),
            engine_factory=engine_factory,
            sessionmaker_factory=sessionmaker_factory,
            text_factory=lambda statement: statement,
        )

        manager.connect()
        health = manager.health_check()

        self.assertTrue(manager.is_connected)
        self.assertEqual(health.status, HealthStatus.HEALTHY)

    def test_missing_sqlalchemy_dependency_is_clear(self) -> None:
        settings = load_database_settings({}, Path(".")).postgresql
        manager = PostgreSQLConnectionManager(settings=settings, logger=_NullLogger())

        with self.assertRaises(DatabaseDependencyError):
            manager.connect()


class DuckDBConnectionManagerTests(unittest.TestCase):
    def test_rejects_mutating_statements(self) -> None:
        with tempfile.NamedTemporaryFile() as handle:
            settings = load_database_settings(
                {"DUCKDB_PATH": handle.name},
                Path("."),
            ).duckdb
            manager = DuckDBConnectionManager(
                settings=settings,
                logger=_NullLogger(),
                connector=lambda **_kwargs: _FakeDuckDBConnection(),
            )
            manager.connect()

            with self.assertRaises(DatabaseWritePolicyError):
                manager.execute_read("INSERT INTO sample VALUES (1)")

    def test_missing_read_only_file_fails_before_dependency_import(self) -> None:
        settings = load_database_settings(
            {"DUCKDB_PATH": "missing-file.duckdb"},
            Path("."),
        ).duckdb
        manager = DuckDBConnectionManager(settings=settings, logger=_NullLogger())

        with self.assertRaises(DatabaseConnectionError):
            manager.connect()


class RedisCacheManagerTests(unittest.TestCase):
    def test_cache_manager_round_trips_json_values(self) -> None:
        settings = load_database_settings({}, Path(".")).redis
        fake_client = _FakeRedisClient()
        manager = RedisConnectionManager(
            settings=settings,
            logger=_NullLogger(),
            redis_factory=lambda *_args, **_kwargs: fake_client,
        )
        manager.connect()
        cache = RedisCacheManager(manager)

        cache.set("alpha", {"value": 1}, ttl_seconds=10)

        self.assertEqual(cache.get("alpha"), {"value": 1})
        self.assertEqual(cache.invalidate_prefix("a"), 1)
        self.assertIsNone(cache.get("alpha"))


class TransactionManagerTests(unittest.TestCase):
    def test_transaction_commits_and_closes(self) -> None:
        session = _FakeSession()
        manager = TransactionManager(lambda: session)

        with manager.transaction() as active:
            self.assertIs(active, session)

        self.assertTrue(session.committed)
        self.assertTrue(session.closed)

    def test_transaction_rolls_back_on_error(self) -> None:
        session = _FakeSession()
        manager = TransactionManager(lambda: session)

        with self.assertRaises(Exception):
            with manager.transaction():
                raise RuntimeError("fail")

        self.assertTrue(session.rolled_back)
        self.assertTrue(session.closed)


class MigrationManagerTests(unittest.TestCase):
    def test_missing_alembic_dependency_is_clear_when_config_exists(self) -> None:
        settings = load_database_settings({}, Path.cwd()).migrations
        manager = create_database_module(
            create_application_context(environ={"APP_ENV": "testing", "LOG_FORMAT": "text"}),
            project_root=Path.cwd(),
            environ={},
        ).migrations

        self.assertEqual(manager.settings.config_path, settings.config_path)
        with self.assertRaises(DatabaseDependencyError):
            manager.build_config()

    def test_missing_alembic_config_fails(self) -> None:
        settings = load_database_settings(
            {"ALEMBIC_CONFIG_PATH": "missing.ini"},
            Path("."),
        )
        manager = create_database_module(
            create_application_context(environ={"APP_ENV": "testing", "LOG_FORMAT": "text"}),
            project_root=Path("."),
            environ={},
            settings=settings,
        ).migrations

        with self.assertRaises(DatabaseMigrationError):
            manager.build_config()


class FoundationIntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_database_module_registers_foundation_services(self) -> None:
        context = create_application_context(
            environ={"APP_ENV": "testing", "LOG_FORMAT": "text"}
        )
        module = create_database_module(context, project_root=Path.cwd(), environ={})

        self.assertIs(context.container.resolve("database.settings"), module.settings)
        self.assertIn("postgresql", context.database_manager.registered_names())
        self.assertIn("database.configuration", context.health_checker.registered_names())

        results = await context.health_checker.run_all()
        statuses = {result.name: result.status for result in results}

        self.assertEqual(statuses["database.configuration"], HealthStatus.HEALTHY)
        self.assertEqual(statuses["database.postgresql"], HealthStatus.UNKNOWN)
        self.assertEqual(statuses["database.duckdb"], HealthStatus.UNKNOWN)
        self.assertEqual(statuses["database.redis"], HealthStatus.UNKNOWN)


class _NullLogger:
    def info(self, *_args: object, **_kwargs: object) -> None:
        return None


class _FakeEngine:
    def __init__(self) -> None:
        self.disposed = False

    def connect(self) -> "_FakeConnection":
        return _FakeConnection()

    def dispose(self) -> None:
        self.disposed = True


class _FakeConnection:
    def __enter__(self) -> "_FakeConnection":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def execute(self, _statement: object) -> None:
        return None


class _FakeSession:
    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

    def close(self) -> None:
        self.closed = True


class _FakeDuckDBConnection:
    def execute(self, _statement: str, _parameters: object) -> "_FakeDuckDBConnection":
        return self

    def fetchall(self) -> list[tuple[int]]:
        return [(1,)]

    def close(self) -> None:
        return None


class _FakeRedisClient:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}

    def ping(self) -> bool:
        return True

    def get(self, key: str) -> str | None:
        return self.values.get(key)

    def setex(self, key: str, _ttl: int, value: str) -> None:
        self.values[key] = value

    def delete(self, *keys: str) -> int:
        count = 0
        for key in keys:
            if key in self.values:
                count += 1
                del self.values[key]
        return count

    def scan_iter(self, match: str) -> list[str]:
        prefix = match.removesuffix("*")
        return [key for key in self.values if key.startswith(prefix)]

    def close(self) -> None:
        return None


if __name__ == "__main__":
    unittest.main()
