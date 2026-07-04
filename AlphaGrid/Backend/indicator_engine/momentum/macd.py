import numpy as np
from Backend.math.public.ema import calculate_ema
from Backend.math.public.diff import calculate_diff
from Backend.market_data.market_series import MarketSeries
from Backend.indicator_engine.results import MACDResult
from Backend.indicator_engine.registry import IndicatorRegistry

class MACDEngine:
    """Financial composition logic for Moving Average Convergence Divergence."""
    
    metadata = {
        "id": "macd",
        "family": "momentum",
        "indicator_type": "oscillator",
        "composable": True,
        "streaming_supported": False,
        "formula": "EMA(close, fast) - EMA(close, slow)",
        "inputs": ["close"],
        "outputs": ["macd", "signal", "histogram"],
        "warmup": "slow_period + signal_period",
        "complexity": "O(N)",
        "deterministic": True,
    }
    
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        self.fast = fast_period
        self.slow = slow_period
        self.signal = signal_period

    def generate(self, series: MarketSeries) -> MACDResult:
        # Calculate fast and slow EMAs
        fast_ema_res = calculate_ema(series.closes, series.timestamps, self.fast, "close")
        slow_ema_res = calculate_ema(series.closes, series.timestamps, self.slow, "close")
        
        # MACD Line = Fast - Slow
        with np.errstate(invalid='ignore'):
            macd_line = fast_ema_res.values - slow_ema_res.values
        
        # Calculate Signal Line = EMA of MACD Line
        signal_res = calculate_ema(macd_line, series.timestamps, self.signal, "macd")
        
        # Histogram = MACD Line - Signal Line
        histogram = macd_line - signal_res.values
        
        return MACDResult(
            timestamps=series.timestamps,
            valid_mask=signal_res.valid_mask,
            warmup_period=self.slow + self.signal - 2,  # TA-Lib strict warmup equivalent
            lookback=self.slow + self.signal - 1,
            metadata=self.metadata,
            macd=macd_line,
            signal=signal_res.values,
            histogram=histogram
        )

# Register engine
IndicatorRegistry.register("macd", MACDEngine, MACDResult)
