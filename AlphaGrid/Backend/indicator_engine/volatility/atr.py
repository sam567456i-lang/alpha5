import numpy as np
from Backend.market_data.market_series import MarketSeries
from Backend.indicator_engine.results import ATRResult
from Backend.indicator_engine.registry import IndicatorRegistry
from Backend.math.public.true_range import calculate_true_range
from Backend.math.public.rma import calculate_rma
from Backend.math.public.ema import calculate_ema
from Backend.math.public.sma import calculate_sma

class ATREngine:
    metadata = {
        "id": "atr",
        "family": "volatility",
        "indicator_type": "volatility",
        "composable": True,
        "streaming_supported": False,
        "formula": "RMA(TrueRange, period)",
        "inputs": ["high", "low", "close"],
        "outputs": ["atr"],
        "warmup": "period",
        "complexity": "O(N)",
        "deterministic": True,
    }
    
    def __init__(self, period: int = 14, smoothing: str = "rma"):
        self.period = period
        self.smoothing = smoothing.lower()

    def generate(self, series: MarketSeries) -> ATRResult:
        tr_res = calculate_true_range(series.highs, series.lows, series.closes, series.timestamps)
        
        if self.smoothing == "rma":
            atr_res = calculate_rma(tr_res.values, series.timestamps, self.period, "tr")
        elif self.smoothing == "ema":
            atr_res = calculate_ema(tr_res.values, series.timestamps, self.period, "tr")
        elif self.smoothing == "sma":
            atr_res = calculate_sma(tr_res.values, series.timestamps, self.period, "tr")
        else:
            raise ValueError(f"Unsupported ATR smoothing type: {self.smoothing}")
            
        return ATRResult(
            timestamps=series.timestamps,
            valid_mask=atr_res.valid_mask,
            warmup_period=self.period,
            lookback=self.period + 1,
            metadata=self.metadata,
            atr=atr_res.values
        )

IndicatorRegistry.register("atr", ATREngine, ATRResult)
