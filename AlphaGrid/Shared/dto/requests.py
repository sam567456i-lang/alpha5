"""Request DTO models."""

from decimal import Decimal
from uuid import UUID
from pydantic import Field, field_validator
from Shared.enums import TradeDirection
from Shared.models.common import AlphaGridBaseModel


class LoginRequest(AlphaGridBaseModel):
    """User authentication login request payload."""

    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class CreatePortfolioRequest(AlphaGridBaseModel):
    """Payload to create a new portfolio."""

    name: str = Field(..., min_length=1)
    initial_capital: Decimal

    @field_validator("initial_capital", mode="after")
    @classmethod
    def validate_capital(cls, v: Decimal) -> Decimal:
        """Ensure starting capital is non-negative."""
        if v < Decimal("0"):
            raise ValueError("Initial capital must be non-negative.")
        return v


class CreateTradeRequest(AlphaGridBaseModel):
    """Payload to create and log a manual trade execution."""

    portfolio_id: UUID
    symbol: str = Field(..., min_length=1)
    trade_type: TradeDirection
    quantity: int
    entry_price: Decimal

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


class CreateRecommendationRequest(AlphaGridBaseModel):
    """Payload to create a new recommendation from an opportunity."""

    opportunity_id: UUID
    strategy: str = Field(..., min_length=1)
    direction: TradeDirection
    entry_price: Decimal
    stop_loss: Decimal
    targets: list[Decimal] = Field(..., min_items=1)

    @field_validator("entry_price", "stop_loss", mode="after")
    @classmethod
    def validate_positive_prices(cls, v: Decimal) -> Decimal:
        """Ensure entry price and stop loss are positive."""
        if v <= Decimal("0"):
            raise ValueError("Price values must be greater than zero.")
        return v

    @field_validator("targets", mode="after")
    @classmethod
    def validate_targets(cls, v: list[Decimal]) -> list[Decimal]:
        """Ensure all target prices are positive."""
        for target in v:
            if target <= Decimal("0"):
                raise ValueError("Target prices must be greater than zero.")
        return v


class CreateResearchProjectRequest(AlphaGridBaseModel):
    """Payload to create a new research project."""

    title: str = Field(..., min_length=1)
    objective: str = Field(..., min_length=1)
