"""Market domain service shim.

This shim replaces the Phase 5 stub. It instantiates the concrete 
MarketService from the Backend.market engine and forwards all calls to it,
preserving the exact method signatures expected by the router.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from Backend.market import ConnectorManager, MarketService as CoreMarketService
from Backend.market.providers.yahoo import YahooFinanceProvider

# We instantiate the core engine here for simplicity in the shim.
# In a full DI container setup, this would be injected.
_manager = ConnectorManager()
_manager.register(YahooFinanceProvider())
_core_service = CoreMarketService(_manager)


@dataclass(frozen=True, slots=True)
class MarketStatus:
    """Current market session state."""

    is_open: bool
    session: str
    exchange: str
    message: str


class MarketService:
    """Shim over the concrete Market Intelligence engine."""

    def get_market_status(self) -> MarketStatus:
        res = _core_service.get_market_status()
        return MarketStatus(
            is_open=res["is_open"],
            session=res["session"],
            exchange=res["exchange"],
            message=f"Server time: {res['server_time']}"
        )

    def get_instruments(
        self, exchange: str | None = None, segment: str | None = None
    ) -> list[dict[str, Any]]:
        return _core_service.get_instruments(exchange, segment)

    def get_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> list[dict[str, Any]]:
        # The core service requires actual dates, so we provide defaults if omitted
        from datetime import datetime, timezone, timedelta
        if not from_date:
            from_date = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        if not to_date:
            to_date = datetime.now(timezone.utc).isoformat()
            
        return _core_service.get_ohlcv(symbol, timeframe, from_date, to_date)

    def get_live_quotes(self, symbols: list[str] | None = None) -> list[dict[str, Any]]:
        if not symbols:
            # Default fallback for testing
            symbols = ["NIFTY", "BANKNIFTY", "RELIANCE"]
        return _core_service.get_live_quotes(symbols)

    def get_market_breadth(self) -> dict[str, Any]:
        return _core_service.get_market_breadth()

    def get_market_regime(self) -> dict[str, Any]:
        return _core_service.get_market_regime()

    def get_economic_calendar(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        return _core_service.get_economic_calendar()

    def get_news(self, limit: int = 20, category: str | None = None) -> list[dict[str, Any]]:
        return _core_service.get_news(limit, category)
