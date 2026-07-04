import numpy as np
from Backend.indicator_engine.results import AccumulationDistributionResult
from Backend.math.public.ad import calculate_ad

class AccumulationDistributionEngine:
    @staticmethod
    def compute(high: np.ndarray, low: np.ndarray, close: np.ndarray, volume: np.ndarray, timestamps: np.ndarray) -> AccumulationDistributionResult:
        res = calculate_ad(high, low, close, volume, timestamps)
        
        return AccumulationDistributionResult(
            timestamps=res.timestamps,
            valid_mask=res.valid_mask,
            warmup_period=res.warmup_period,
            lookback=1,
            metadata={"indicator": "Accumulation/Distribution"},
            ad=res.values
        )
