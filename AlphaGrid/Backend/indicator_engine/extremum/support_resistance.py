import numpy as np
from Backend.indicator_engine.results import SupportResistanceResult
from Backend.math.public.rolling_max import calculate_rolling_max
from Backend.math.public.rolling_min import calculate_rolling_min

class SupportResistanceEngine:
    """
    Computes rolling support and resistance levels without introducing new math primitives.
    Outputs purely numerical distances to these levels rather than semantic flags.
    """
    @staticmethod
    def compute(close: np.ndarray, high: np.ndarray, low: np.ndarray, timestamps: np.ndarray, period: int = 50) -> SupportResistanceResult:
        if period <= 0:
            raise ValueError("Period must be > 0")
            
        resistance = calculate_rolling_max(high, timestamps, period).values
        support = calculate_rolling_min(low, timestamps, period).values
        
        with np.errstate(invalid='ignore', divide='ignore'):
            dist_res = (resistance - close) / close
            dist_sup = (close - support) / close
            
        valid_mask = ~np.isnan(resistance)
        
        return SupportResistanceResult(
            timestamps=timestamps,
            valid_mask=valid_mask,
            warmup_period=period - 1,
            lookback=period,
            metadata={"period": period},
            resistance=resistance,
            support=support,
            distance_to_resistance=dist_res,
            distance_to_support=dist_sup
        )
