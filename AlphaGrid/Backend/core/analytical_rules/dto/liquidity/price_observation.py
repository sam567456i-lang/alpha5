from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class PriceObservationDTO:
    """
    Methodology-agnostic representation of a chronological price sample.
    Can wrap a Tick, Candle, Bar, or Replay Record.
    """
    observation_id: str
    timestamp: str
    high: float
    low: float
    open: float
    close: float
    volume: float = 0.0
    observation_type: str = "CANDLE" # "TICK", "CANDLE", "BAR"
    metadata: Dict[str, Any] = None
