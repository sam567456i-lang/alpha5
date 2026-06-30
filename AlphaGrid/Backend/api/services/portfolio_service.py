"""Portfolio service stub.

Interface contract for the portfolio domain. Real implementation belongs in
the Portfolio Engine phase.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any
from uuid import UUID

from Shared.enums import TradeDirection


class PortfolioService:
    """Stub service for portfolio domain operations."""

    def get_portfolio(self) -> dict[str, Any]:
        """Return the current portfolio summary including positions and PnL."""
        return {
            "capital": "0.00",
            "invested_amount": "0.00",
            "unrealized_pnl": "0.00",
            "realized_pnl": "0.00",
            "open_trades": [],
            "closed_trades": [],
            "positions": [],
        }

    def add_trade(
        self,
        symbol: str,
        trade_type: TradeDirection,
        quantity: int,
        entry_price: Decimal,
        portfolio_id: UUID | None = None,
        notes: str | None = None,
    ) -> dict[str, Any]:
        """Record a new manual trade and return the created trade record."""
        return {
            "status": "created",
            "symbol": symbol,
            "trade_type": str(trade_type),
            "quantity": quantity,
            "entry_price": str(entry_price),
        }

    def update_trade(
        self, trade_id: UUID, updates: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Update an existing trade record. Returns updated record or None if not found."""
        return None

    def archive_trade(self, trade_id: UUID) -> bool:
        """Soft-archive a trade. Returns True if the trade was found and archived."""
        return False
