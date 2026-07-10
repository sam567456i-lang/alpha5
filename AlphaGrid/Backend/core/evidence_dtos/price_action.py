from dataclasses import dataclass, field
from typing import List, Optional
from Backend.core.evidence_dtos.base import BasePlatformObject

@dataclass
class BasePriceActionObject(BasePlatformObject):
    """
    Root base for Price Action candlestick math objects.
    Produces ONLY objective geometric evidence. NO bullish/bearish opinions.
    """
    pa_uuid: str = ""
    member_bar_timestamps: List[float] = field(default_factory=list)
    geometric_upper_bound: float = 0.0
    geometric_lower_bound: float = 0.0

# --- Single Candle Objects ---
@dataclass
class PinBar(BasePriceActionObject):
    wick_percentage: float = 0.0

@dataclass
class Hammer(BasePriceActionObject):
    lower_wick_percentage: float = 0.0

@dataclass
class Doji(BasePriceActionObject):
    open_close_distance: float = 0.0

@dataclass
class Marubozu(BasePriceActionObject):
    body_percentage: float = 0.0

@dataclass
class SpinningTop(BasePriceActionObject):
    body_percentage: float = 0.0

# --- Two Candle Objects ---
@dataclass
class Engulfing(BasePriceActionObject):
    engulfed_percentage: float = 0.0

@dataclass
class Harami(BasePriceActionObject):
    inside_percentage: float = 0.0

@dataclass
class Tweezer(BasePriceActionObject):
    alignment_deviation: float = 0.0

# --- Three Candle Objects ---
@dataclass
class MorningStar(BasePriceActionObject):
    middle_bar_distance: float = 0.0

@dataclass
class ThreeWhiteSoldiers(BasePriceActionObject):
    sequence_expansion_rate: float = 0.0

# --- Range & Momentum Objects ---
@dataclass
class InsideBar(BasePriceActionObject):
    compression_ratio: float = 0.0

@dataclass
class OutsideBar(BasePriceActionObject):
    expansion_ratio: float = 0.0

@dataclass
class NR4(BasePriceActionObject):
    """Narrowest Range of the last 4 bars."""
    range_value: float = 0.0

@dataclass
class NR7(BasePriceActionObject):
    """Narrowest Range of the last 7 bars."""
    range_value: float = 0.0

@dataclass
class ExpansionCandle(BasePriceActionObject):
    expansion_multiple: float = 0.0

@dataclass
class ExhaustionCandle(BasePriceActionObject):
    wick_expansion_ratio: float = 0.0
