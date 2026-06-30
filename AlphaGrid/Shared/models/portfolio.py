"""Portfolio domain shared models."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import Field, field_validator
from Shared.enums import TradeDirection, TradeStatus
from .common import AlphaGridBaseModel


class Portfolio(AlphaGridBaseModel):
    """Trading portfolio tracking assets and PnL."""

    portfolio_id: UUID
    name: str = Field(..., min_length=1)
    capital: Decimal
    invested_amount: Decimal
    unrealized_pnl: Decimal
    realized_pnl: Decimal
    created_at: datetime

    @field_validator("capital", mode="after")
    @classmethod
    def validate_capital(cls, v: Decimal) -> Decimal:
        """Ensure starting capital is non-negative."""
        if v < Decimal("0"):
            raise ValueError("Capital must be non-negative.")
        return v


class Position(AlphaGridBaseModel):
    """An active holding in a portfolio."""

    position_id: UUID
    portfolio_id: UUID
    symbol: str = Field(..., min_length=1)
    quantity: int
    average_price: Decimal
    current_price: Decimal
    unrealized_pnl: Decimal

    @field_validator("quantity", mode="after")
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        """Ensure position quantity is greater than zero."""
        if v <= 0:
            raise ValueError("Quantity must be greater than zero.")
        return v

    @field_validator("average_price", "current_price", mode="after")
    @classmethod
    def validate_prices(cls, v: Decimal) -> Decimal:
        """Ensure prices are non-negative."""
        if v < Decimal("0"):
            raise ValueError("Price values must be non-negative.")
        return v


class Trade(AlphaGridBaseModel):
    """An execution log of a manual trade."""

    trade_id: UUID
    portfolio_id: UUID
    recommendation_id: UUID | None = Field(default=None)
    symbol: str = Field(..., min_length=1)
    trade_type: TradeDirection
    quantity: int
    entry_price: Decimal
    exit_price: Decimal | None = Field(default=None)
    execution_time: datetime
    status: TradeStatus

    @field_validator("quantity", mode="after")
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        """Ensure trade quantity is greater than zero."""
        if v <= 0:
            raise ValueError("Quantity must be greater than zero.")
        return v

    @field_validator("entry_price", mode="after")
    @classmethod
    def validate_entry_price(cls, v: Decimal) -> Decimal:
        """Ensure entry price is positive."""
        if v <= Decimal("0"):
            raise ValueError("Entry price must be greater than zero.")
        return v

    @field_validator("exit_price", mode="after")
    @classmethod
    def validate_exit_price(cls, v: Decimal | None) -> Decimal | None:
        """Ensure exit price is positive if provided."""
        if v is not None and v <= Decimal("0"):
            raise ValueError("Exit price must be greater than zero.")
        return v
