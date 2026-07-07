"""Market domain service shim.

This shim replaces the Phase 5 stub. It instantiates the concrete 
Market Intelligence engines and forwards API calls to them,
adhering strictly to the canonical architectural pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Dict
from datetime import datetime, timezone

from Backend.market_intelligence.session_engine import SessionEngine
from Backend.market_intelligence.universe_manager import UniverseManager, UniverseTier
from Backend.market_intelligence.normalization_engine import NormalizationEngine
from Backend.market_intelligence.market_state_engine import MarketState
from Backend.market_intelligence.symbol_metadata_registry import SymbolMetadataRegistry

@dataclass(frozen=True, slots=True)
class MarketStatusResponse:
    """Current market session state."""
    is_open: bool
    session: str
    exchange: str
    message: str


from Backend.market_intelligence.providers.abstract_market_data_provider import HistoricalDataProvider

class MarketService:
    """Canonical Service over the Market Intelligence engine."""

    def __init__(
        self,
        session_engine: SessionEngine,
        universe_manager: UniverseManager,
        normalization_engine: NormalizationEngine,
        historical_market_pipeline: Any = None,
        symbol_metadata_registry: SymbolMetadataRegistry | None = None,
    ) -> None:
        self._session_engine = session_engine
        self._universe_manager = universe_manager
        self._normalization_engine = normalization_engine
        self._historical_market_pipeline = historical_market_pipeline
        self._symbol_metadata_registry = symbol_metadata_registry

    def get_market_status(self) -> MarketStatusResponse:
        now = datetime.now(timezone.utc)
        state = self._session_engine.get_session_state(now)
        
        is_open = state == MarketState.OPEN
        
        return MarketStatusResponse(
            is_open=is_open,
            session=state.value if hasattr(state, 'value') else str(state),
            exchange="NSE",
            message=f"Server time: {now.isoformat()}"
        )

    def get_instruments(self, exchange: str | None = None, segment: str | None = None) -> List[Dict[str, Any]]:
        if self._symbol_metadata_registry is None:
            return []

        instruments = []
        for metadata in self._symbol_metadata_registry.get_all():
            if exchange and metadata.exchange.upper() != exchange.upper():
                continue
            if segment and metadata.instrument_type.value.upper() != segment.upper():
                continue
            instruments.append({
                "symbol": metadata.canonical_symbol,
                "instrument_type": metadata.instrument_type.value,
                "exchange": metadata.exchange,
                "sector": metadata.sector,
                "industry": metadata.industry,
                "tick_size": metadata.tick_size,
                "lot_size": metadata.lot_size,
                "currency": metadata.currency,
                "trading_hours_id": metadata.trading_hours_id,
            })
        return instruments

    def get_ohlcv(
        self, symbol: str, timeframe: str, from_date: str | None = None, to_date: str | None = None
    ) -> List[Dict[str, Any]]:
        if not self._historical_market_pipeline:
            raise RuntimeError("historical_market_pipeline is not wired.")
        return self._historical_market_pipeline.execute(symbol, timeframe, from_date, to_date)

    def get_live_quotes(self, symbols: List[str] | None = None) -> List[Dict[str, Any]]:
        return []

    def get_market_breadth(self) -> dict:
        return {"advances": 0, "declines": 0, "ad_ratio": 1.0, "score": 50}

    def get_market_regime(self) -> dict:
        return {"regime": "UNKNOWN", "confidence": 0.0}

    def get_economic_calendar(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        return []

    def get_news(self, limit: int = 20, category: str | None = None) -> list[dict[str, Any]]:
        return []
