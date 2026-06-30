# Database

Database infrastructure for AlphaGrid Infinity X 5.0.

## Scope

This module provides:

- Database settings and validation
- PostgreSQL connection manager, pool configuration, and session factory
- DuckDB read-only analytics connection manager
- Redis cache connection and cache manager
- Alembic migration configuration and environment
- SQLAlchemy migration base metadata
- Generic repository and transaction primitives
- Foundation health and dependency-injection registration

## Ownership Rules

- PostgreSQL is the persistent source of truth.
- DuckDB is read-only from the application and is reserved for analytical projections.
- Redis is a temporary cache only and never owns persistent data.
- No business tables or business repositories are created in this module.

## Configuration

Database settings are read from environment variables. Secrets must be provided
outside source control.

Required operational values:

- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DUCKDB_PATH`
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_PASSWORD`

Optional infrastructure values:

- `POSTGRES_POOL_SIZE`
- `POSTGRES_MAX_OVERFLOW`
- `POSTGRES_POOL_TIMEOUT_SECONDS`
- `POSTGRES_ECHO_SQL`
- `DUCKDB_READ_ONLY`
- `REDIS_DB`
- `REDIS_DEFAULT_TTL_SECONDS`
- `REDIS_SOCKET_TIMEOUT_SECONDS`
- `ALEMBIC_CONFIG_PATH`
- `ALEMBIC_SCRIPT_LOCATION`

## Migrations

Alembic files live in:

```text
Database/alembic.ini
Database/migrations/env.py
Database/migrations/script.py.mako
Database/schema/base.py
```

The migration base declares metadata only. Business table migrations must be
introduced by later approved modules.
