from dataclasses import dataclass
from typing import Dict
from Backend.market_data.market_bar import MarketBar

@dataclass(frozen=True)
class MarketSnapshot:
    """Immutable contract representing a cross-sectional snapshot of the market at a single point in time."""
    timestamp: int
    bars: Dict[str, MarketBar]  # symbol -> MarketBar
