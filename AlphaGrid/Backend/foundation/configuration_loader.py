"""Configuration loading for the AlphaGrid foundation module."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
from typing import Mapping

from .constants import (
    APP_NAME,
    DEFAULT_ENVIRONMENT,
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOG_LEVEL,
    ENV_PREFIX,
    VALID_ENVIRONMENTS,
    VALID_LOG_FORMATS,
)
from .exceptions import ConfigurationError


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Validated runtime settings required by the foundation module."""

    app_name: str
    environment: str
    log_level: str
    log_format: str
    service_timeout_seconds: float
    health_timeout_seconds: float
    shutdown_timeout_seconds: float

    def as_dict(self) -> dict[str, str | float]:
        """Return a serializable representation of the configuration."""

        return {
            "app_name": self.app_name,
            "environment": self.environment,
            "log_level": self.log_level,
            "log_format": self.log_format,
            "service_timeout_seconds": self.service_timeout_seconds,
            "health_timeout_seconds": self.health_timeout_seconds,
            "shutdown_timeout_seconds": self.shutdown_timeout_seconds,
        }


def load_config(
    env_file: str | Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> AppConfig:
    """Load and validate foundation configuration from environment values.

    Values from ``environ`` override values read from ``env_file``. When
    ``environ`` is omitted, the process environment is used.
    """

    file_values = _read_env_file(env_file) if env_file is not None else {}
    runtime_values = dict(os.environ if environ is None else environ)
    values = {**file_values, **runtime_values}

    environment = _read_string(values, "APP_ENV", DEFAULT_ENVIRONMENT).lower()
    if environment not in VALID_ENVIRONMENTS:
        allowed = ", ".join(sorted(VALID_ENVIRONMENTS))
        raise ConfigurationError(
            f"APP_ENV must be one of: {allowed}. Received: {environment!r}."
        )

    log_format = _read_string(values, "LOG_FORMAT", DEFAULT_LOG_FORMAT).lower()
    if log_format not in VALID_LOG_FORMATS:
        allowed = ", ".join(sorted(VALID_LOG_FORMATS))
        raise ConfigurationError(
            f"LOG_FORMAT must be one of: {allowed}. Received: {log_format!r}."
        )

    return AppConfig(
        app_name=_read_string(values, "APP_NAME", APP_NAME),
        environment=environment,
        log_level=_read_string(values, "LOG_LEVEL", DEFAULT_LOG_LEVEL).upper(),
        log_format=log_format,
        service_timeout_seconds=_read_float(values, "SERVICE_TIMEOUT_SECONDS", 30.0),
        health_timeout_seconds=_read_float(values, "HEALTH_TIMEOUT_SECONDS", 5.0),
        shutdown_timeout_seconds=_read_float(values, "SHUTDOWN_TIMEOUT_SECONDS", 30.0),
    )


def _read_string(values: Mapping[str, str], key: str, default: str) -> str:
    direct = values.get(key)
    prefixed = values.get(f"{ENV_PREFIX}{key}")
    value = prefixed if prefixed is not None else direct
    if value is None or value.strip() == "":
        return default
    return value.strip()


def _read_float(values: Mapping[str, str], key: str, default: float) -> float:
    raw_value = _read_string(values, key, str(default))
    try:
        value = float(raw_value)
    except ValueError as exc:
        raise ConfigurationError(f"{key} must be a number.") from exc
    if value <= 0:
        raise ConfigurationError(f"{key} must be greater than zero.")
    return value


def _read_env_file(env_file: str | Path) -> dict[str, str]:
    path = Path(env_file)
    if not path.exists():
        raise ConfigurationError(f"Environment file does not exist: {path}")
    if not path.is_file():
        raise ConfigurationError(f"Environment path is not a file: {path}")

    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if line == "" or line.startswith("#"):
            continue
        if "=" not in line:
            raise ConfigurationError(
                f"Invalid environment file line {line_number}: expected KEY=VALUE."
            )
        key, value = line.split("=", 1)
        key = key.strip()
        if key == "":
            raise ConfigurationError(
                f"Invalid environment file line {line_number}: empty key."
            )
        values[key] = _strip_optional_quotes(value.strip())
    return values


def _strip_optional_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value
