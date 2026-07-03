"""Trading Decision Objects."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

@dataclass(frozen=True)
class TradingDecision:
    """
    Final decision emitted by a Strategy before being sent to Risk/Portfolio/Evidence.
    """
    strategy_id: str
    timestamp: datetime
    action: str  # e.g., 'BUY', 'SELL', 'HOLD'
    confidence: float
    metadata: Dict[str, Any]
