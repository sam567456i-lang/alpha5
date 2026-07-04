import numpy as np
from Backend.indicator_engine.results import HighLowResult
from Backend.math.public.rolling_max import calculate_rolling_max
from Backend.math.public.rolling_min import calculate_rolling_min
from Backend.math.public.shift import calculate_shift

class HighLowEngine:
    @staticmethod
    def compute(high: np.ndarray, low: np.ndarray, timestamps: np.ndarray, period: int = 14) -> HighLowResult:
        if period <= 0:
            raise ValueError("Period must be > 0")
            
        # High/Low breakout uses the *previous* period's highest high / lowest low
        raw_upper = calculate_rolling_max(high, timestamps, period).values
        raw_lower = calculate_rolling_min(low, timestamps, period).values
        
        highest_high = calculate_shift(raw_upper, timestamps, period=1).values
        lowest_low = calculate_shift(raw_lower, timestamps, period=1).values
        
        valid_mask = ~np.isnan(highest_high)
        
        return HighLowResult(
            timestamps=timestamps,
            valid_mask=valid_mask,
            warmup_period=period,  # shift adds 1
            lookback=period + 1,
            metadata={"period": period},
            highest_high=highest_high,
            lowest_low=lowest_low
        )
