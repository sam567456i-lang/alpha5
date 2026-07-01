"""Dataset snapshot model for the Research Platform."""

from datetime import datetime, timezone
from pydantic import Field, field_validator
from Shared.models.common import AlphaGridBaseModel


class DatasetSnapshot(AlphaGridBaseModel):
    """Immutable representation of historical OHLCV data for reproducibility."""

    snapshot_id: str = Field(..., min_length=64, max_length=64, description="Canonical SHA-256 hash")
    canonical_hash: str = Field(..., min_length=64, max_length=64, description="Explicit canonical hash for pre-load verification")
    provider: str = Field(..., min_length=1)
    symbol: str = Field(..., min_length=1)
    timeframe: str = Field(..., min_length=1)
    adjustment_mode: str = Field(..., min_length=1)
    timezone: str = Field(default="UTC", frozen=True)
    start_date: datetime
    end_date: datetime
    storage_path: str = Field(..., min_length=1)
    row_count: int = Field(..., ge=0)
    schema_version: int = Field(default=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        """Ensure timezone is strictly UTC."""
        if v.upper() != "UTC":
            raise ValueError("Timezone must be strictly UTC for DatasetSnapshot.")
        return v.upper()

    @field_validator("start_date", "end_date", "created_at")
    @classmethod
    def ensure_utc(cls, v: datetime) -> datetime:
        """Ensure datetimes are timezone-aware and set to UTC."""
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        return v
