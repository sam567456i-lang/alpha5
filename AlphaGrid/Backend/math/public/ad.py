import numpy as np
from numba import njit
from Backend.math.public.indicator_result import IndicatorResult

@njit(cache=True)
def _ad_kernel(high: np.ndarray, low: np.ndarray, close: np.ndarray, volume: np.ndarray) -> np.ndarray:
    n = len(close)
    out = np.empty(n, dtype=np.float64)
    
    if n == 0:
        return out
        
    ad_prev = 0.0
    
    for i in range(n):
        if np.isnan(high[i]) or np.isnan(low[i]) or np.isnan(close[i]) or np.isnan(volume[i]):
            out[i] = np.nan
        else:
            hl_range = high[i] - low[i]
            if hl_range == 0:
                mfm = 0.0
            else:
                mfm = ((close[i] - low[i]) - (high[i] - close[i])) / hl_range
                
            mfv = mfm * volume[i]
            out[i] = ad_prev + mfv
            ad_prev = out[i]
            
    return out

def calculate_ad(high: np.ndarray, low: np.ndarray, close: np.ndarray, volume: np.ndarray, timestamps: np.ndarray) -> IndicatorResult:
    """
    Accumulation/Distribution (A/D) Line.
    """
    if not (len(high) == len(low) == len(close) == len(volume) == len(timestamps)):
        raise ValueError("Inputs must have the same length.")
        
    out = _ad_kernel(high, low, close, volume)
    valid_mask = ~np.isnan(out)
    
    return IndicatorResult(
        values=out,
        timestamps=timestamps,
        valid_mask=valid_mask,
        warmup_period=1,
        metadata={"indicator": "Accumulation/Distribution"}
    )
