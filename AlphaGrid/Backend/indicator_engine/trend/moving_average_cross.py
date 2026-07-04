import numpy as np
from Backend.market_data.market_series import MarketSeries
from Backend.indicator_engine.results import MACrossResult
from Backend.indicator_engine.registry import IndicatorRegistry
from Backend.indicator_engine.runner import IndicatorRunner

class MACrossEngine:
    metadata = {
        "id": "ma_cross",
        "family": "trend",
        "indicator_type": "composite",
        "composable": False,
        "streaming_supported": False,
        "formula": "FastMA - SlowMA",
        "inputs": ["close"],
        "outputs": ["fast_ma", "slow_ma", "cross_signal"],
        "warmup": "max(fast_warmup, slow_warmup)",
        "complexity": "O(N)",
        "deterministic": True,
    }
    
    def __init__(self, fast_period: int = 10, slow_period: int = 30, fast_type: str = "ema", slow_type: str = "ema"):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.fast_type = fast_type
        self.slow_type = slow_type

    def generate(self, series: MarketSeries) -> MACrossResult:
        # Generate underlying primitives via the runner
        fast_res = IndicatorRunner.execute(self.fast_type, series, period=self.fast_period)
        slow_res = IndicatorRunner.execute(self.slow_type, series, period=self.slow_period)
        
        # Determine exactly which array was returned by the fast/slow engine (e.g. res.ema, res.sma, res.wma)
        # We can dynamically get it by checking the metadata outputs or inspecting the result object.
        fast_arr = getattr(fast_res, self.fast_type)
        slow_arr = getattr(slow_res, self.slow_type)
        
        cross_signal = fast_arr - slow_arr
        valid_mask = fast_res.valid_mask & slow_res.valid_mask
        
        return MACrossResult(
            timestamps=series.timestamps,
            valid_mask=valid_mask,
            warmup_period=max(fast_res.warmup_period, slow_res.warmup_period),
            lookback=max(fast_res.lookback, slow_res.lookback),
            metadata=self.metadata,
            fast_ma=fast_arr,
            slow_ma=slow_arr,
            cross_signal=cross_signal
        )

IndicatorRegistry.register("ma_cross", MACrossEngine, MACrossResult)
