"""Options service stub.

Interface contract for the options domain. Real implementation belongs in
the Options Platform phase.
"""

from __future__ import annotations

from typing import Any


class OptionsService:
    """Stub service for options domain operations."""

    def get_option_chain(
        self, symbol: str, expiry: str | None = None
    ) -> list[dict[str, Any]]:
        """Return the full option chain for a given underlying."""
        return []

    def get_greeks(
        self, symbol: str, expiry: str | None = None
    ) -> list[dict[str, Any]]:
        """Return option Greeks for a given underlying and expiry."""
        return []

    def get_implied_volatility(
        self, symbol: str, expiry: str | None = None
    ) -> dict[str, Any]:
        """Return implied volatility surface data."""
        return {"symbol": symbol, "iv_percentile": 0.0, "iv_rank": 0.0}

    def get_pcr(self, symbol: str) -> dict[str, Any]:
        """Return the Put-Call Ratio for a given underlying."""
        return {"symbol": symbol, "pcr": 0.0}

    def get_max_pain(self, symbol: str, expiry: str | None = None) -> dict[str, Any]:
        """Return the Max Pain strike for a given expiry."""
        return {"symbol": symbol, "max_pain_strike": 0.0, "expiry": expiry}
