"""Structured logging utilities for AlphaGrid."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import logging
from typing import Any, Mapping

from .constants import DEFAULT_LOG_FORMAT, DEFAULT_LOG_LEVEL, SECRET_FIELD_MARKERS


class SecretRedactingFilter(logging.Filter):
    """Remove secret-like values from log record extras."""

    def filter(self, record: logging.LogRecord) -> bool:
        for key, value in list(record.__dict__.items()):
            if _is_secret_key(key):
                setattr(record, key, "[REDACTED]")
            elif isinstance(value, Mapping):
                setattr(record, key, redact_mapping(value))
        return True


class JsonFormatter(logging.Formatter):
    """Format logs as compact JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created,
                tz=timezone.utc,
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        for key, value in record.__dict__.items():
            if key in _STANDARD_LOG_RECORD_KEYS:
                continue
            payload[key] = "[REDACTED]" if _is_secret_key(key) else value

        return json.dumps(payload, default=str, separators=(",", ":"))


def configure_logging(
    level: str = DEFAULT_LOG_LEVEL,
    log_format: str = DEFAULT_LOG_FORMAT,
) -> None:
    """Configure root logging once for the application process."""

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(_parse_level(level))

    handler = logging.StreamHandler()
    handler.addFilter(SecretRedactingFilter())
    if log_format == "json":
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S%z",
            )
        )
    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger for a module."""

    if name.strip() == "":
        raise ValueError("Logger name must not be empty.")
    return logging.getLogger(name)


def redact_mapping(values: Mapping[str, Any]) -> dict[str, Any]:
    """Return a copy of ``values`` with secret-like keys redacted."""

    redacted: dict[str, Any] = {}
    for key, value in values.items():
        key_as_string = str(key)
        if _is_secret_key(key_as_string):
            redacted[key_as_string] = "[REDACTED]"
        elif isinstance(value, Mapping):
            redacted[key_as_string] = redact_mapping(value)
        else:
            redacted[key_as_string] = value
    return redacted


def _parse_level(level: str) -> int:
    parsed = logging.getLevelName(level.upper())
    if isinstance(parsed, int):
        return parsed
    raise ValueError(f"Invalid log level: {level!r}")


def _is_secret_key(key: str) -> bool:
    normalized = key.lower()
    return any(marker in normalized for marker in SECRET_FIELD_MARKERS)


_STANDARD_LOG_RECORD_KEYS = frozenset(
    {
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "message",
        "module",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "thread",
        "threadName",
    }
)
