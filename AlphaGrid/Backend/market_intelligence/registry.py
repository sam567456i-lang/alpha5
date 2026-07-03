"""Market Intelligence domain registry hook."""

from Backend.foundation.dependency_injection_container import DependencyContainer
from Backend.market_intelligence.session_engine import SessionEngine
from Backend.market_intelligence.universe_manager import UniverseManager
from Backend.market_intelligence.normalization_engine import NormalizationEngine

def register_market_intelligence_services(container: DependencyContainer) -> None:
    """Registers all Market Intelligence domain engines into the canonical container."""
    container.register_factory(
        "session_engine",
        lambda c: SessionEngine(),
        singleton=True
    )
    container.register_factory(
        "universe_manager",
        lambda c: UniverseManager(),
        singleton=True
    )
    container.register_factory(
        "normalization_engine",
        lambda c: NormalizationEngine(),
        singleton=True
    )
    
    app_config = container.resolve("config")
    
    from Backend.market_intelligence.providers.provider_factory import ProviderFactory
    container.register_factory(
        "historical_data_provider",
        lambda c: ProviderFactory.create(app_config.historical_provider),
        singleton=True
    )
    
    from Backend.market_intelligence.data_quality_gate import DataQualityGate
    container.register_factory(
        "data_quality_gate",
        lambda c: DataQualityGate(),
        singleton=True
    )

    from Backend.market_intelligence.historical_market_pipeline import HistoricalMarketPipeline
    container.register_factory(
        "historical_market_pipeline",
        lambda c: HistoricalMarketPipeline(
            provider=c.resolve("historical_data_provider"),
            normalization_engine=c.resolve("normalization_engine"),
            session_engine=c.resolve("session_engine"),
            data_quality_gate=c.resolve("data_quality_gate")
        ),
        singleton=True
    )
