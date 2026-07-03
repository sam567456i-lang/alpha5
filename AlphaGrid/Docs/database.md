---
Document ID: DOC-002
Title: "Database Module"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Root
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# Database Module

## Purpose

The Database module provides AlphaGrid's storage infrastructure. It defines how
the application connects to PostgreSQL, DuckDB, Redis, and Alembic without
creating business tables or business repositories.

## Dependencies

Runtime dependencies declared in `pyproject.toml`:

- SQLAlchemy
- Alembic
- psycopg
- duckdb
- redis

The module imports these dependencies lazily so tests and static imports can run
before local services or packages are installed.

## Public APIs

- `load_database_settings()` validates database environment configuration.
- `PostgreSQLConnectionManager` owns PostgreSQL engine and session factory setup.
- `DuckDBConnectionManager` owns the read-only analytical DuckDB connection.
- `RedisConnectionManager` owns the Redis client.
- `RedisCacheManager` provides temporary JSON cache helpers.
- `MigrationManager` builds Alembic configuration.
- `TransactionManager` provides generic unit-of-work transaction scopes.
- `CRUDRepository` defines the repository interface for future business modules.
- `BaseRepository` provides generic SQLAlchemy CRUD operations.
- `create_database_module()` registers database infrastructure with Foundation.

## Configuration

Database configuration is environment-driven and documented in `.env.example`.
Secrets are redacted from diagnostic output.

## Health Checks

`create_database_module()` registers:

- `database.configuration`
- `database.postgresql`
- `database.duckdb`
- `database.redis`

Connection-specific health checks report `unknown` when managers are configured
but not connected, allowing infrastructure verification without requiring live
database services.

## Ownership Rules

- PostgreSQL is the source of truth.
- DuckDB is read-only from the application.
- Redis is cache only.
- Projection workers may be introduced later by an approved module.

## Known Limitations

No schema, table, business repository, projection worker, or cache coherence
worker is implemented in this module. Those require later module-specific
specification and tests.
