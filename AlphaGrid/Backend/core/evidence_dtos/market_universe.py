from enum import Enum
from dataclasses import dataclass
from typing import Optional

class TimeAlignmentPolicy(Enum):
    EXACT_TIMESTAMP = "EXACT_TIMESTAMP"
    NEAREST_TIMESTAMP = "NEAREST_TIMESTAMP"
    PREVIOUS_OBSERVATION = "PREVIOUS_OBSERVATION"
    CALENDAR_SESSION = "CALENDAR_SESSION"
    EXCHANGE_SPECIFIC = "EXCHANGE_SPECIFIC"

class MissingDataPolicy(Enum):
    SKIP = "SKIP"
    FORWARD_FILL = "FORWARD_FILL"
    INTERPOLATE = "INTERPOLATE"
    REJECT_CALCULATION = "REJECT_CALCULATION"

@dataclass(frozen=True)
class MarketIdentity:
    """Immutable identity metadata for assets within the MarketUniverse."""
    symbol: str
    exchange: str
    asset_class: str
    currency: str
    trading_calendar: str
    time_zone: str
    tick_size: float
    lot_size: float
    corporate_action_policy: str

@dataclass
class MarketUniverseConfig:
    """Configuration mapping for processing multiple streams simultaneously."""
    target_asset: MarketIdentity
    benchmarks: list[MarketIdentity]
    alignment_policy: TimeAlignmentPolicy = TimeAlignmentPolicy.PREVIOUS_OBSERVATION
    missing_data_policy: MissingDataPolicy = MissingDataPolicy.FORWARD_FILL
