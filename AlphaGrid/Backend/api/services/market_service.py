"""Market service stub.

This is a typed interface contract. Real market logic will be implemented
in Backend/market/ during the Market Platform phase. Routers call this
service exclusively — they never touch the database or external APIs directly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class MarketStatus:
    """Current market session state."""

    is_open: bool
    session: str
    exchange: str
    message: str


class MarketService:
    """Stub service for market domain operations."""

    def get_market_status(self) -> MarketStatus:
        """Return the current market session status."""
        return MarketStatus(
            is_open=False,
            session="CLOSED",
            exchange="NSE",
            message="Market service not yet implemented. Stub response.",
        )

    def get_instruments(
        self, exchange: str | None = None, segment: str | None = None
    ) -> list[dict[str, Any]]:
        """Return the tradable instrument catalog."""
        return []

    def get_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return historical OHLCV candles for a given symbol and timeframe."""
        return []

    def get_live_quotes(
        self, symbols: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """Return the latest live price quotes."""
        return []

    def get_market_breadth(self) -> dict[str, Any]:
        """Return current market breadth metrics."""
        return {
            "advances": 0,
            "declines": 0,
            "unchanged": 0,
            "advance_decline_ratio": 0.0,
            "breadth_score": 0.0,
        }

    def get_market_regime(self) -> dict[str, Any]:
        """Return the currently detected market regime."""
        return {
            "regime": "UNKNOWN",
            "confidence": 0.0,
            "trend_strength": 0.0,
            "volatility_score": 0.0,
        }

    def get_economic_calendar(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """Return upcoming macroeconomic events."""
        return []

    def get_news(
        self, limit: int = 20, category: str | None = None
    ) -> list[dict[str, Any]]:
        """Return recent market news articles."""
        return []
