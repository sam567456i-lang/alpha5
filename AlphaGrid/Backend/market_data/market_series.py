from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class MarketSeries:
    """Immutable contract representing a historical timeseries of OHLCV bars."""
    symbol: str
    timeframe: str
    timestamps: np.ndarray  # int64
    opens: np.ndarray       # float64
    highs: np.ndarray       # float64
    lows: np.ndarray        # float64
    closes: np.ndarray      # float64
    volumes: np.ndarray     # float64
    
    def __post_init__(self):
        n = len(self.timestamps)
        if not (len(self.opens) == len(self.highs) == len(self.lows) == len(self.closes) == len(self.volumes) == n):
            raise ValueError("All arrays in MarketSeries must have identical lengths.")
        
    def __len__(self) -> int:
        return len(self.timestamps)
