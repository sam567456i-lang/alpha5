"""Concrete MarketService — delegates API router requests to market engines."""

from __future__ import annotations

from typing import Any
from datetime import datetime, timezone

from Shared.models.market import MarketSnapshot

from .breadth import MarketBreadthCalculator
from .connector_manager import ConnectorManager
from .instruments import InstrumentCatalog
from .live_quotes import LiveQuoteEngine
from .ohlcv import OHLCVEngine
from .regime import RegimeDetector
from .session import MarketSessionManager


class MarketService:
    """Core market intelligence service.
    
    This replaces the stub in Backend/api/services/market_service.py.
    """

    def __init__(self, connector_manager: ConnectorManager) -> None:
        self.manager = connector_manager
        self.catalog = InstrumentCatalog(self.manager)
        self.ohlcv_engine = OHLCVEngine(self.manager, self.catalog)
        self.quote_engine = LiveQuoteEngine(self.manager, self.catalog)
        self.session_manager = MarketSessionManager()

    def get_market_status(self) -> dict[str, Any]:
        """Return current market session and exchange status."""
        session = self.session_manager.current_session("NSE")
        is_open = self.session_manager.is_market_open("NSE")
        
        return {
            "is_open": is_open,
            "session": session,
            "exchange": "NSE",
            "server_time": datetime.now(timezone.utc).isoformat(),
        }

    def get_instruments(
        self, exchange: str | None, segment: str | None
    ) -> list[dict[str, Any]]:
        """Return a filtered list of supported instruments."""
        instruments = self.catalog.get_all(exchange, segment)
        # Convert dataclasses to dicts for the API layer
        return [
            {
                "symbol": i.symbol,
                "exchange": i.exchange,
                "segment": i.segment,
                "name": i.display_name,
            }
            for i in instruments
        ]

    def get_ohlcv(
        self, symbol: str, timeframe: str, from_date: str, to_date: str
    ) -> list[dict[str, Any]]:
        """Return historical OHLCV data."""
        try:
            from_dt = datetime.fromisoformat(from_date)
            to_dt = datetime.fromisoformat(to_date)
        except ValueError:
            # Fallback if the router passed short dates
            from_dt = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            to_dt = datetime.strptime(to_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)

        snapshots = self.ohlcv_engine.get_ohlcv(symbol, timeframe, from_dt, to_dt)
        return [s.model_dump() for s in snapshots]

    def get_live_quotes(self, symbols: list[str]) -> list[dict[str, Any]]:
        """Return real-time price snapshots."""
        snapshots = self.quote_engine.get_live_quotes(symbols)
        return [s.model_dump() for s in snapshots]

    def get_market_breadth(self) -> dict[str, Any]:
        """Calculate market breadth metrics."""
        # Typically we'd fetch quotes for a known index constituent list.
        # For demonstration, we'll fetch our default mock symbols.
        symbols = ["NIFTY", "BANKNIFTY", "RELIANCE", "HDFCBANK", "TCS"]
        quotes = self.quote_engine.get_live_quotes(symbols)
        return MarketBreadthCalculator.calculate_breadth(quotes)

    def get_market_regime(self) -> dict[str, Any]:
        """Detect current market regime."""
        breadth = self.get_market_breadth()
        b_score = breadth.get("breadth_score", 0.5)
        
        # In a real system, VIX and Trend would be fetched from the engine.
        # We stub VIX=14.5 and Trend=0.55 here to demonstrate the detection.
        return RegimeDetector.detect_regime(
            breadth_score=b_score,
            vix_value=14.5,
            trend_strength=0.55,
        )

    def get_economic_calendar(self) -> list[dict[str, Any]]:
        """Return upcoming economic events."""
        # This belongs in a News/Event provider, stubbed for now to fulfill the contract.
        return [
            {
                "event": "RBI Policy Decision",
                "date": "2026-08-10T10:00:00Z",
                "impact": "HIGH",
            }
        ]

    def get_news(self, limit: int, category: str | None) -> list[dict[str, Any]]:
        """Return market news."""
        # Stubbed
        return [
            {
                "headline": "Markets hit new highs",
                "source": "Reuters",
                "time": datetime.now(timezone.utc).isoformat(),
            }
        ]
