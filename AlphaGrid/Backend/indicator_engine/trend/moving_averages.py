import numpy as np
from Backend.math.public.sma import calculate_sma
from Backend.math.public.ema import calculate_ema
from Backend.math.public.wma import calculate_wma
from Backend.market_data.market_series import MarketSeries
from Backend.indicator_engine.results import SMAResult, EMAResult, WMAResult
from Backend.indicator_engine.registry import IndicatorRegistry

class SMAEngine:
    metadata = {
        "id": "sma",
        "family": "trend",
        "indicator_type": "moving_average",
        "composable": True,
        "streaming_supported": False,
        "formula": "Sum(close, n) / n",
        "inputs": ["close"],
        "outputs": ["sma"],
        "warmup": "period - 1",
        "complexity": "O(N)",
        "deterministic": True,
    }
    
    def __init__(self, period: int = 20):
        self.period = period

    def generate(self, series: MarketSeries) -> SMAResult:
        res = calculate_sma(series.closes, series.timestamps, self.period, "close")
        return SMAResult(
            timestamps=series.timestamps,
            valid_mask=res.valid_mask,
            warmup_period=self.period - 1,
            lookback=self.period,
            metadata=self.metadata,
            sma=res.values
        )

class EMAEngine:
    metadata = {
        "id": "ema",
        "family": "trend",
        "indicator_type": "moving_average",
        "composable": True,
        "streaming_supported": False,
        "formula": "Price(t) * k + EMA(y) * (1-k)",
        "inputs": ["close"],
        "outputs": ["ema"],
        "warmup": "period",
        "complexity": "O(N)",
        "deterministic": True,
    }
    
    def __init__(self, period: int = 20):
        self.period = period

    def generate(self, series: MarketSeries) -> EMAResult:
        res = calculate_ema(series.closes, series.timestamps, self.period, "close")
        return EMAResult(
            timestamps=series.timestamps,
            valid_mask=res.valid_mask,
            warmup_period=self.period,
            lookback=self.period + 1,
            metadata=self.metadata,
            ema=res.values
        )

class WMAEngine:
    metadata = {
        "id": "wma",
        "family": "trend",
        "indicator_type": "moving_average",
        "composable": True,
        "streaming_supported": False,
        "formula": "Sum(Price * Weight) / Sum(Weights)",
        "inputs": ["close"],
        "outputs": ["wma"],
        "warmup": "period - 1",
        "complexity": "O(N)",
        "deterministic": True,
    }
    
    def __init__(self, period: int = 20):
        self.period = period

    def generate(self, series: MarketSeries) -> WMAResult:
        res = calculate_wma(series.closes, series.timestamps, self.period, "close")
        return WMAResult(
            timestamps=series.timestamps,
            valid_mask=res.valid_mask,
            warmup_period=self.period - 1,
            lookback=self.period,
            metadata=self.metadata,
            wma=res.values
        )

IndicatorRegistry.register("sma", SMAEngine, SMAResult)
IndicatorRegistry.register("ema", EMAEngine, EMAResult)
IndicatorRegistry.register("wma", WMAEngine, WMAResult)
