from dataclasses import dataclass
from enum import Enum

class LiquidityLevelType(Enum):
    EQUAL_HIGH = "EQUAL_HIGH"
    EQUAL_LOW = "EQUAL_LOW"
    TRIPLE_TOP = "TRIPLE_TOP"
    TRIPLE_BOTTOM = "TRIPLE_BOTTOM"
    CLUSTER_HIGH = "CLUSTER_HIGH"
    CLUSTER_LOW = "CLUSTER_LOW"

class ToleranceType(Enum):
    TICKS = "TICKS"
    ATR = "ATR"

@dataclass
class LiquidityLevelPolicy:
    """Configurable policy dictating how a resting liquidity pool is identified."""
    tolerance_value: float = 0.10
    tolerance_type: ToleranceType = ToleranceType.ATR
    min_touches: int = 2
    max_touches: int = 5
    lookback_window: int = 100
