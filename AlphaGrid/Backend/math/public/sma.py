import numpy as np
from typing import Any, Dict
from Backend.math.public.indicator_result import IndicatorResult
from Backend.math.public.ema import _build_empty_result

def calculate_sma(
    values: np.ndarray,
    timestamps: np.ndarray,
    period: int,
    input_column: str = "close"
) -> IndicatorResult:
    """
    Simple Moving Average (SMA) - Pure NumPy float64 Implementation.
    """
    if not isinstance(values, np.ndarray):
        values = np.asarray(values, dtype=np.float64)
        
    n = len(values)
    out = np.full(n, np.nan, dtype=np.float64)
    valid_mask = np.zeros(n, dtype=bool)
    
    if n < period:
        return _build_empty_result(values, timestamps, period, input_column, "Insufficient data")
        
    # Use np.convolve for fast sliding window mean, handling NaNs gracefully
    # We will build a manual loop for pure NaN-robustness, or use convolve if clean.
    # For safety in Institutional contexts with NaNs, a manual rolling sum or 
    # specialized function is safer.
    
    window_sum = 0.0
    valid_count = 0
    
    for i in range(n):
        if not np.isnan(values[i]):
            window_sum += values[i]
            valid_count += 1
            
        if i >= period:
            if not np.isnan(values[i - period]):
                window_sum -= values[i - period]
                valid_count -= 1
                
        if valid_count == period:
            out[i] = window_sum / period
            valid_mask[i] = True
            
    return IndicatorResult(
        values=out,
        timestamps=timestamps,
        valid_mask=valid_mask,
        warmup_period=period - 1,
        lookback=period,
        input_columns=[input_column],
        parameters={"period": period},
        metadata={
            "name": "Simple Moving Average",
            "short_name": "SMA",
            "inputs": ["close"],
            "output": ["values"],
            "warmup": period - 1,
            "deterministic": True,
            "precision": "1e-12",
            "complexity": "O(N)",
            "memory": "O(N)",
            "supports_nan": True,
            "supports_inf": True,
            "supports_streaming": False,
            "supports_incremental": False,
        },
        complexity="O(n)",
        memory_complexity="O(n)",
        version="1.0.0",
        warnings=[],
        statistics={
            "nan_count": int(np.sum(np.isnan(out))),
            "valid_count": int(np.sum(valid_mask))
        }
    )


def update_sma(bar: Any, state: Dict[str, Any]) -> Any:
    raise NotImplementedError("Streaming API reserved for future implementation.")
