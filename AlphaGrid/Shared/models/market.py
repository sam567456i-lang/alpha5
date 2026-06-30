"""Market domain shared models."""

from datetime import datetime
from decimal import Decimal
from pydantic import Field, field_validator
from .common import AlphaGridBaseModel


class MarketSnapshot(AlphaGridBaseModel):
    """Real-time market snapshot for an instrument."""

    symbol: str = Field(..., min_length=1)
    exchange: str = Field(..., min_length=1)
    instrument_type: str = Field(..., min_length=1)
    last_price: Decimal
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    bid: Decimal | None = Field(default=None)
    ask: Decimal | None = Field(default=None)
    timestamp: datetime

    @field_validator("last_price", "open", "high", "low", "close", "bid", "ask", mode="after")
    @classmethod
    def validate_non_negative_decimal(cls, v: Decimal | None) -> Decimal | None:
        """Ensure prices and bid/ask fields are non-negative."""
        if v is not None and v < Decimal("0"):
            raise ValueError("Price values must be non-negative.")
        return v

    @field_validator("volume", mode="after")
    @classmethod
    def validate_non_negative_int(cls, v: int) -> int:
        """Ensure volume is non-negative."""
        if v < 0:
            raise ValueError("Volume must be non-negative.")
        return v

    @field_validator("timestamp", mode="after")
    @classmethod
    def validate_utc_timestamp(cls, v: datetime) -> datetime:
        """Ensure timestamp is timezone-aware."""
        if v.tzinfo is None:
            raise ValueError("Timestamp must be timezone-aware.")
        return v
