# Foundation Module

## Purpose

The Foundation module provides the infrastructure used by later AlphaGrid
modules. It does not implement trading logic, APIs, database schemas, shared
models, AI models, or frontend screens.

## Public APIs

- `create_application_context()` builds the foundation context.
- `load_config()` loads validated runtime settings from an env file and process
  environment.
- `configure_logging()` configures structured logging with secret redaction.
- `DependencyContainer` registers and resolves services by explicit names.
- `EventBus` publishes immutable event envelopes that match the approved event
  contract.
- `HealthChecker` registers and executes sync or async health checks.
- `LifecycleManager` coordinates startup and shutdown callbacks.
- `DatabaseManager` tracks externally created database resources for health and
  graceful close operations.
- `PluginLoader` imports plugin modules and invokes an optional `register`
  function.

## Dependencies

The module uses only the Python standard library. External platform dependencies
are declared in `pyproject.toml` for future modules.

## Configuration

Supported environment values:

- `APP_ENV`
- `APP_NAME`
- `LOG_LEVEL`
- `LOG_FORMAT`
- `SERVICE_TIMEOUT_SECONDS`
- `HEALTH_TIMEOUT_SECONDS`
- `SHUTDOWN_TIMEOUT_SECONDS`

Each value may also be provided with the `ALPHAGRID_` prefix.

## Known Limitations

The Foundation module intentionally does not open PostgreSQL, DuckDB, or Redis
connections. Concrete database connections, repositories, migrations, and schema
management belong to the Database module.
