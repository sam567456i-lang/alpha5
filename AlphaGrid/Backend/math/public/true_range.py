import numpy as np
from typing import Optional
import time
from Backend.math.public.indicator_result import IndicatorResult
from Backend.math.public.shift import calculate_shift
from Backend.math.public.validation import sanitize_input

def calculate_true_range(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    timestamps: np.ndarray,
) -> IndicatorResult:
    """
    Computes the True Range (TR).
    TR = max(High - Low, abs(High - PrevClose), abs(Low - PrevClose))
    """
    start_time = time.perf_counter()

    if not isinstance(high, np.ndarray) or not isinstance(low, np.ndarray) or not isinstance(close, np.ndarray):
        raise TypeError("Inputs must be numpy arrays")

    if high.ndim != 1 or low.ndim != 1 or close.ndim != 1:
        raise ValueError("Inputs must be 1D numpy arrays")

    if len(high) != len(low) or len(high) != len(close) or len(high) != len(timestamps):
        raise ValueError("Inputs must have identical length")

    if len(high) == 0:
        raise ValueError("Inputs cannot be empty")
    
    # 1. High - Low
    tr1 = high - low
    
    # 2. High - PrevClose
    prev_close_res = calculate_shift(close, timestamps, period=1)
    prev_close = prev_close_res.values
    tr2 = np.abs(high - prev_close)
    
    # 3. Low - PrevClose
    tr3 = np.abs(low - prev_close)
    
    # max of tr1, tr2, tr3
    true_range = np.maximum(tr1, np.maximum(tr2, tr3))
    
    # Handle the first value (where prev_close is NaN)
    # Typically TR at t=0 is just High - Low
    if len(true_range) > 0:
        true_range[0] = tr1[0]
        
    valid_mask = ~np.isnan(true_range) & ~np.isinf(true_range)
    
    duration = time.perf_counter() - start_time
    
    return IndicatorResult(
        values=true_range,
        timestamps=timestamps,
        valid_mask=valid_mask,
        warmup_period=1,
        lookback=2,
        input_columns=["high", "low", "close"],
        parameters={},
        metadata={
            "description": "True Range",
            "execution_time_ms": duration * 1000.0,
            "deterministic": True
        },
        complexity="O(N)",
        memory_complexity="O(N)",
        version="1.0"
    )
