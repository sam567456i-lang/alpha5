import numpy as np
from Backend.indicator_engine.results import OBVResult
from Backend.math.public.obv import calculate_obv

class OBVEngine:
    @staticmethod
    def compute(close: np.ndarray, volume: np.ndarray, timestamps: np.ndarray) -> OBVResult:
        res = calculate_obv(close, volume, timestamps)
        
        return OBVResult(
            timestamps=res.timestamps,
            valid_mask=res.valid_mask,
            warmup_period=res.warmup_period,
            lookback=2, # Needs previous close
            metadata={"indicator": "OBV"},
            obv=res.values
        )
