"""Foundation constants."""

from __future__ import annotations

APP_NAME = "AlphaGrid Infinity X 5.0"
DEFAULT_ENVIRONMENT = "development"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "json"
ENV_PREFIX = "ALPHAGRID_"

VALID_ENVIRONMENTS = frozenset({"development", "testing", "production"})
VALID_LOG_FORMATS = frozenset({"json", "text"})

SECRET_FIELD_MARKERS = frozenset(
    {
        "api_key",
        "apikey",
        "authorization",
        "password",
        "secret",
        "token",
    }
)
