import numpy as np
from Backend.indicator_engine.results import VolumeSMAResult
from Backend.math.public.sma import calculate_sma

class VolumeSMAEngine:
    @staticmethod
    def compute(volume: np.ndarray, timestamps: np.ndarray, period: int = 20) -> VolumeSMAResult:
        if period <= 0:
            raise ValueError("Period must be > 0")
            
        res = calculate_sma(volume, timestamps, period)
        
        return VolumeSMAResult(
            timestamps=res.timestamps,
            valid_mask=res.valid_mask,
            warmup_period=res.warmup_period,
            lookback=period,
            metadata={"indicator": "Volume SMA", "period": period},
            volume_sma=res.values
        )
