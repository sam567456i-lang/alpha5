from dataclasses import dataclass
from typing import Dict
from Backend.market_data.market_series import MarketSeries

@dataclass(frozen=True)
class MarketDataset:
    """Immutable contract representing historical timeseries for multiple symbols."""
    timeframe: str
    series: Dict[str, MarketSeries]  # symbol -> MarketSeries
