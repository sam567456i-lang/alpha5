from dataclasses import dataclass
from Backend.core.evidence_dtos.base import BasePlatformObject
from Backend.core.interfaces.profile_framework import ProfileIdentity

# --- Measurements ---
@dataclass
class TPOHistogramMeasurement:
    """Read-only measurement representing time-at-price."""
    price_levels: dict # price -> number of TPO blocks

# --- Objects (Derived States) ---
@dataclass
class MarketProfileObject(BasePlatformObject):
    """
    Root base for Market Profile (Time-based) concepts.
    """
    profile_uuid: str = ""
    # We remove 'identity: ProfileIdentity = None' to avoid breaking dataclass inheritance.
    # The identity field is inherited from BasePlatformObject (which is a PlatformIdentity).
    # Downstream engines will just supply the correct identity instance.

@dataclass
class TPO_POC(MarketProfileObject):
    price_level: float = 0.0
    tpo_count: int = 0

@dataclass
class ValueArea(MarketProfileObject):
    vah_price: float = 0.0
    val_price: float = 0.0
    poc_price: float = 0.0

@dataclass
class InitialBalance(MarketProfileObject):
    high_price: float = 0.0
    low_price: float = 0.0

@dataclass
class SinglePrints(MarketProfileObject):
    price_levels: list = None

@dataclass
class Excess(MarketProfileObject):
    is_buying_tail: bool = True
    tail_length: float = 0.0
