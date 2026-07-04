import numpy as np
from Backend.indicator_engine.results import DonchianResult
from Backend.math.public.rolling_max import calculate_rolling_max
from Backend.math.public.rolling_min import calculate_rolling_min

class DonchianEngine:
    @staticmethod
    def compute(high: np.ndarray, low: np.ndarray, timestamps: np.ndarray, period: int = 20) -> DonchianResult:
        if period <= 0:
            raise ValueError("Period must be > 0")
            
        upper_res = calculate_rolling_max(high, timestamps, period)
        lower_res = calculate_rolling_min(low, timestamps, period)
        
        upper = upper_res.values
        lower = lower_res.values
        
        # Avoid warnings on NaNs
        with np.errstate(invalid='ignore'):
            middle = (upper + lower) / 2.0
            bandwidth = (upper - lower) / middle
            
        valid_mask = ~np.isnan(upper)
        
        return DonchianResult(
            timestamps=timestamps,
            valid_mask=valid_mask,
            warmup_period=period - 1,
            lookback=period,
            metadata={"period": period},
            upper=upper,
            lower=lower,
            middle=middle,
            bandwidth=bandwidth
        )
