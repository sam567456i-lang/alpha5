import numpy as np
from numba import njit
from Backend.math.public.indicator_result import IndicatorResult

@njit(cache=True)
def _obv_kernel(close: np.ndarray, volume: np.ndarray) -> np.ndarray:
    n = len(close)
    out = np.empty(n, dtype=np.float64)
    
    if n == 0:
        return out
        
    out[0] = volume[0]
    
    for i in range(1, n):
        if np.isnan(close[i]) or np.isnan(volume[i]) or np.isnan(close[i-1]):
            out[i] = np.nan
        else:
            if close[i] > close[i-1]:
                out[i] = out[i-1] + volume[i]
            elif close[i] < close[i-1]:
                out[i] = out[i-1] - volume[i]
            else:
                out[i] = out[i-1]
                
    return out

def calculate_obv(close: np.ndarray, volume: np.ndarray, timestamps: np.ndarray) -> IndicatorResult:
    """
    On-Balance Volume (OBV).
    """
    if len(close) != len(volume) or len(close) != len(timestamps):
        raise ValueError("Inputs must have the same length.")
        
    out = _obv_kernel(close, volume)
    valid_mask = ~np.isnan(out)
    
    return IndicatorResult(
        values=out,
        timestamps=timestamps,
        valid_mask=valid_mask,
        warmup_period=1,
        metadata={"indicator": "OBV"}
    )
