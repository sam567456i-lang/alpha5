from dataclasses import dataclass
from enum import Enum
from typing import Optional

class BOSConfirmationMethod(Enum):
    WICK = "WICK"
    CLOSE = "CLOSE"
    CONSECUTIVE_CLOSES = "CONSECUTIVE_CLOSES"

class BOSPenetrationType(Enum):
    TICKS = "TICKS"
    ATR = "ATR"
    PERCENTAGE = "PERCENTAGE"

@dataclass
class BOSPolicy:
    """Configurable policy dictating how a Break of Structure is confirmed."""
    confirmation_method: BOSConfirmationMethod = BOSConfirmationMethod.CLOSE
    minimum_penetration: float = 0.0
    penetration_type: BOSPenetrationType = BOSPenetrationType.TICKS
    consecutive_closes_required: int = 1
    lookback_window: int = 50
    equal_high_tolerance_ticks: int = 0
