"""AlphaGrid foundation module public API."""

from .application_entrypoint import ApplicationContext, create_application_context
from .configuration_loader import AppConfig, load_config
from .database_manager import DatabaseManager, DatabaseResource
from .dependency_injection_container import DependencyContainer, ServiceRegistry
from .event_bus import EventBus, EventEnvelope
from .exceptions import (
    AlphaGridError,
    ConfigurationError,
    EventBusError,
    HealthCheckError,
    LifecycleError,
    PluginLoadError,
    ServiceRegistrationError,
    ServiceResolutionError,
)
from .health_checker import HealthChecker, HealthCheckResult, HealthStatus
from .lifecycle_manager import LifecycleManager, LifecycleState
from .logger import configure_logging, get_logger, redact_mapping
from .plugin_loader import LoadedPlugin, PluginLoader

__all__ = [
    "AlphaGridError",
    "AppConfig",
    "ApplicationContext",
    "ConfigurationError",
    "DatabaseManager",
    "DatabaseResource",
    "DependencyContainer",
    "EventBus",
    "EventBusError",
    "EventEnvelope",
    "HealthCheckError",
    "HealthCheckResult",
    "HealthChecker",
    "HealthStatus",
    "LifecycleError",
    "LifecycleManager",
    "LifecycleState",
    "LoadedPlugin",
    "PluginLoadError",
    "PluginLoader",
    "ServiceRegistry",
    "ServiceRegistrationError",
    "ServiceResolutionError",
    "configure_logging",
    "create_application_context",
    "get_logger",
    "load_config",
    "redact_mapping",
]
