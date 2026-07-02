"""Strategy Definitions Initialization."""

from .rsi_reversion import RSI_REVERSION
from .bollinger_reversion import BOLLINGER_REVERSION
from .supertrend_cross import SUPERTREND_CROSS

__all__ = [
    "RSI_REVERSION",
    "BOLLINGER_REVERSION",
    "SUPERTREND_CROSS"
]
