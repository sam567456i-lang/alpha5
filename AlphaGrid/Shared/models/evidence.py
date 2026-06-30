"""Evidence domain shared models."""

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID
from pydantic import Field, field_validator
from .common import AlphaGridBaseModel


class Evidence(AlphaGridBaseModel):
    """Real-time intelligence evidence supporting recommendations."""

    evidence_id: UUID
    version: int
    source: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    instrument: str = Field(..., min_length=1)
    timeframe: str = Field(..., min_length=1)
    confidence: Decimal
    weight: Decimal
    score: Decimal
    explanation: str = Field(..., min_length=1)
    timestamp: datetime
    metadata: dict[str, Any] | None = Field(default=None)

    @field_validator("confidence", "weight", mode="after")
    @classmethod
    def validate_fraction(cls, v: Decimal) -> Decimal:
        """Ensure confidence and weight are bounded between 0.0 and 1.0."""
        if v < Decimal("0") or v > Decimal("1"):
            raise ValueError("Value must be between 0.0 and 1.0 (inclusive).")
        return v
