import numpy as np
from Backend.market_data.market_series import MarketSeries
from Backend.indicator_engine.results import KeltnerResult
from Backend.indicator_engine.registry import IndicatorRegistry
from Backend.indicator_engine.runner import IndicatorRunner

class KeltnerEngine:
    metadata = {
        "id": "keltner",
        "family": "volatility",
        "indicator_type": "bands",
        "composable": True,
        "streaming_supported": False,
        "formula": "Middle = EMA(close, n), Upper = Middle + k * ATR, Lower = Middle - k * ATR",
        "inputs": ["high", "low", "close"],
        "outputs": ["upper", "middle", "lower"],
        "warmup": "max(period, atr_period)",
        "complexity": "O(N)",
        "deterministic": True,
    }
    
    def __init__(self, period: int = 20, atr_period: int = 10, multiplier: float = 2.0):
        self.period = period
        self.atr_period = atr_period
        self.multiplier = multiplier

    def generate(self, series: MarketSeries) -> KeltnerResult:
        ema_res = IndicatorRunner.execute("ema", series, period=self.period)
        atr_res = IndicatorRunner.execute("atr", series, period=self.atr_period, smoothing="rma")
        
        middle = ema_res.ema
        atr = atr_res.atr
        
        upper = middle + (self.multiplier * atr)
        lower = middle - (self.multiplier * atr)
        
        valid_mask = ema_res.valid_mask & atr_res.valid_mask
        
        return KeltnerResult(
            timestamps=series.timestamps,
            valid_mask=valid_mask,
            warmup_period=max(ema_res.warmup_period, atr_res.warmup_period),
            lookback=max(ema_res.lookback, atr_res.lookback),
            metadata=self.metadata,
            upper=upper,
            middle=middle,
            lower=lower
        )

IndicatorRegistry.register("keltner", KeltnerEngine, KeltnerResult)
