"""Foundation exception hierarchy."""

from __future__ import annotations


class AlphaGridError(Exception):
    """Base exception for recoverable AlphaGrid application errors."""


class ConfigurationError(AlphaGridError):
    """Raised when runtime configuration is invalid or unavailable."""


class ServiceRegistrationError(AlphaGridError):
    """Raised when a dependency cannot be registered safely."""


class ServiceResolutionError(AlphaGridError):
    """Raised when a dependency cannot be resolved."""


class EventBusError(AlphaGridError):
    """Raised when event publication or subscription fails."""


class HealthCheckError(AlphaGridError):
    """Raised when a health check is invalid or cannot execute."""


class LifecycleError(AlphaGridError):
    """Raised when startup or shutdown lifecycle management fails."""


class PluginLoadError(AlphaGridError):
    """Raised when a plugin module cannot be loaded or registered."""
