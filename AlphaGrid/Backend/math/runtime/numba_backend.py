import numpy as np

# Fail import immediately if numba is missing
import numba
from numba import njit

@njit(cache=True)
def _numba_ema_loop(values: np.ndarray, out: np.ndarray, valid_mask: np.ndarray, start_idx: int, alpha: float):
    n = len(values)
    prev_ema = out[start_idx]
    
    for i in range(start_idx + 1, n):
        if np.isnan(values[i]):
            out[i] = np.nan
            prev_ema = np.nan
        else:
            if np.isnan(prev_ema):
                prev_ema = values[i]
            current_ema = (values[i] * alpha) + (prev_ema * (1.0 - alpha))
            out[i] = current_ema
            valid_mask[i] = True
            prev_ema = current_ema

class NumbaBackend:
    def ema_loop(self, values: np.ndarray, out: np.ndarray, valid_mask: np.ndarray, start_idx: int, alpha: float) -> None:
        _numba_ema_loop(values, out, valid_mask, start_idx, alpha)
