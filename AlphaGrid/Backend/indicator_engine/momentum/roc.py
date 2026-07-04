import numpy as np
from Backend.math.public.roc import calculate_roc
from Backend.market_data.market_series import MarketSeries
from Backend.indicator_engine.results import ROCResult
from Backend.indicator_engine.registry import IndicatorRegistry

class ROCEngine:
    """Financial composition logic for Rate of Change."""
    
    metadata = {
        "id": "roc",
        "family": "momentum",
        "indicator_type": "oscillator",
        "composable": True,
        "streaming_supported": False,
        "formula": "((Price(t) - Price(t-n)) / Price(t-n)) * 100",
        "inputs": ["close"],
        "outputs": ["roc"],
        "warmup": "period",
        "complexity": "O(N)",
        "deterministic": True,
    }
    
    def __init__(self, period: int = 14):
        self.period = period

    def generate(self, series: MarketSeries) -> ROCResult:
        roc_res = calculate_roc(series.closes, series.timestamps, self.period, "close")
        
        return ROCResult(
            timestamps=series.timestamps,
            valid_mask=roc_res.valid_mask,
            warmup_period=self.period,
            lookback=self.period + 1,
            metadata=self.metadata,
            roc=roc_res.values
        )

# Register engine
IndicatorRegistry.register("roc", ROCEngine, ROCResult)
