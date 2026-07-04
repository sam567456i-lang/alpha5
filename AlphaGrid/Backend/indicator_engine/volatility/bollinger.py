import numpy as np
from Backend.market_data.market_series import MarketSeries
from Backend.indicator_engine.results import BollingerResult
from Backend.indicator_engine.registry import IndicatorRegistry
from Backend.math.public.sma import calculate_sma
from Backend.math.public.stddev import calculate_stddev

class BollingerEngine:
    metadata = {
        "id": "bollinger",
        "family": "volatility",
        "indicator_type": "bands",
        "composable": True,
        "streaming_supported": False,
        "formula": "Middle = SMA(close, n), Upper = Middle + k * StdDev, Lower = Middle - k * StdDev",
        "inputs": ["close"],
        "outputs": ["upper", "middle", "lower", "bandwidth", "percent_b"],
        "warmup": "period - 1",
        "complexity": "O(N)",
        "deterministic": True,
    }
    
    def __init__(self, period: int = 20, std_dev: float = 2.0):
        self.period = period
        self.std_dev = std_dev

    def generate(self, series: MarketSeries) -> BollingerResult:
        sma_res = calculate_sma(series.closes, series.timestamps, self.period, "close")
        stddev_res = calculate_stddev(series.closes, series.timestamps, self.period, "close")
        
        middle = sma_res.values
        std = stddev_res.values
        
        upper = middle + (self.std_dev * std)
        lower = middle - (self.std_dev * std)
        
        # Bandwidth = (Upper - Lower) / Middle
        with np.errstate(divide='ignore', invalid='ignore'):
            bandwidth = (upper - lower) / middle
            # %B = (Price - Lower) / (Upper - Lower)
            percent_b = (series.closes - lower) / (upper - lower)
            
        valid_mask = sma_res.valid_mask & stddev_res.valid_mask
        
        return BollingerResult(
            timestamps=series.timestamps,
            valid_mask=valid_mask,
            warmup_period=self.period - 1,
            lookback=self.period,
            metadata=self.metadata,
            upper=upper,
            middle=middle,
            lower=lower,
            bandwidth=bandwidth,
            percent_b=percent_b
        )

IndicatorRegistry.register("bollinger", BollingerEngine, BollingerResult)
