"""Foundation application context assembly."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import logging
from typing import Mapping

from .configuration_loader import load_config
from .database_manager import DatabaseManager
from .dependency_injection_container import DependencyContainer
from .event_bus import EventBus
from .health_checker import HealthChecker, HealthCheckResult, HealthStatus
from .lifecycle_manager import LifecycleManager
from .logger import configure_logging, get_logger


@dataclass(frozen=True, slots=True)
class ApplicationContext:
    """Foundation services required by later AlphaGrid modules."""

    config: AppConfig
    logger: logging.Logger
    container: DependencyContainer
    event_bus: EventBus
    database_manager: DatabaseManager
    health_checker: HealthChecker
    lifecycle_manager: LifecycleManager


def create_application_context(
    env_file: str | Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> ApplicationContext:
    """Create and register the foundation application context."""

    config = load_config(env_file=env_file, environ=environ)
    configure_logging(level=config.log_level, log_format=config.log_format)
    logger = get_logger("alphagrid.foundation")
    container = DependencyContainer()
    event_bus = EventBus()
    database_manager = DatabaseManager()
    health_checker = HealthChecker(timeout_seconds=config.health_timeout_seconds)
    lifecycle_manager = LifecycleManager(logger=logger)

    context = ApplicationContext(
        config=config,
        logger=logger,
        container=container,
        event_bus=event_bus,
        database_manager=database_manager,
        health_checker=health_checker,
        lifecycle_manager=lifecycle_manager,
    )

    _register_foundation_services(context)
    
    from Backend.market_intelligence.registry import register_market_intelligence_services
    register_market_intelligence_services(container)
    
    from Backend.features.registry_hook import register_features
    register_features(container)
    
    from Backend.concepts.registry_hook import register_concepts
    register_concepts(container)
    
    from Backend.signals.primitive.registry_hook import register_primitive_signals
    register_primitive_signals(container)
    
    from Backend.methodology.registry_hook import register_methodologies
    register_methodologies(container)
    
    from Backend.strategy.registry_hook import register_strategies
    register_strategies(container)
    
    from Backend.evidence.registry_hook import register_evidence
    register_evidence(container)
    
    from Backend.core.canonical_pipeline import DomainResearchPipeline
    from Backend.market_intelligence.historical_market_pipeline import HistoricalMarketPipeline
    from Backend.features.engine import FeatureEngine
    # We deliberately resolve concept_engine dynamically inside the pipeline 
    # to ensure it crashes AT the exact execution boundary.
    container.register_factory("domain_research_pipeline", lambda c: DomainResearchPipeline(
        historical_market_pipeline=c.resolve("historical_market_pipeline", HistoricalMarketPipeline),
        feature_engine=c.resolve("feature_engine", FeatureEngine),
        container=c
    ), singleton=True)
    
    return context


def _register_foundation_services(context: ApplicationContext) -> None:
    context.container.register_instance("config", context.config)
    context.container.register_instance("logger", context.logger)
    context.container.register_instance("event_bus", context.event_bus)
    context.container.register_instance("database_manager", context.database_manager)
    context.container.register_instance("health_checker", context.health_checker)
    context.container.register_instance("lifecycle_manager", context.lifecycle_manager)

    context.health_checker.register(
        "foundation.context",
        lambda: HealthCheckResult(
            name="foundation.context",
            status=HealthStatus.HEALTHY,
            message="Foundation context is initialized.",
        ),
    )
