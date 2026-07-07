"""Market Intelligence domain registry hook."""

from Backend.foundation.dependency_injection_container import DependencyContainer
from Backend.market_intelligence.session_engine import SessionEngine
from Backend.market_intelligence.universe_manager import UniverseManager, UniverseTier
from Backend.market_intelligence.normalization_engine import NormalizationEngine
from Backend.market_intelligence.exchange_contract import NSEImplementation
from Backend.market_intelligence.symbol_metadata_registry import (
    InstrumentType,
    SymbolMetadata,
    SymbolMetadataRegistry,
)


def _build_symbol_metadata_registry() -> SymbolMetadataRegistry:
    registry = SymbolMetadataRegistry()
    for metadata in [
        SymbolMetadata("NIFTY", InstrumentType.INDEX, "NSE", sector="MARKET", tick_size=0.05, lot_size=25),
        SymbolMetadata("BANKNIFTY", InstrumentType.INDEX, "NSE", sector="BANKING", tick_size=0.05, lot_size=15),
        SymbolMetadata("FINNIFTY", InstrumentType.INDEX, "NSE", sector="FINANCIAL_SERVICES", tick_size=0.05, lot_size=40),
        SymbolMetadata("MIDCPNIFTY", InstrumentType.INDEX, "NSE", sector="MARKET", tick_size=0.05, lot_size=75),
        SymbolMetadata("BTCUSDT", InstrumentType.CRYPTO, "SYNTHETIC", sector="CRYPTO", tick_size=0.01, lot_size=1, currency="USDT"),
    ]:
        registry.register(metadata)
    return registry

def register_market_intelligence_services(container: DependencyContainer) -> None:
    """Registers all Market Intelligence domain engines into the canonical container."""
    container.register_factory(
        "exchange_contract",
        lambda c: NSEImplementation(),
        singleton=True
    )
    container.register_factory(
        "symbol_metadata_registry",
        lambda c: _build_symbol_metadata_registry(),
        singleton=True
    )
    container.register_factory(
        "session_engine",
        lambda c: SessionEngine(c.resolve("exchange_contract")),
        singleton=True
    )
    container.register_factory(
        "universe_manager",
        lambda c: _build_universe_manager(c.resolve("symbol_metadata_registry")),
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
    from Backend.market_intelligence.trading_calendar import TradingCalendar
    container.register_factory(
        "trading_calendar",
        lambda c: TradingCalendar(c.resolve("exchange_contract")),
        singleton=True
    )
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


def _build_universe_manager(metadata_registry: SymbolMetadataRegistry) -> UniverseManager:
    manager = UniverseManager(metadata_registry)
    for symbol in ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"]:
        manager.assign_to_tier(symbol, UniverseTier.TIER_A)
    manager.assign_to_tier("BTCUSDT", UniverseTier.TIER_D)
    return manager
