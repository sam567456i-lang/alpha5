import numpy as np
import time
from typing import Dict, Any
from Backend.math.public.indicator_result import IndicatorResult
from Backend.math.runtime.backend import get_backend

def calculate_rma(
    values: np.ndarray,
    timestamps: np.ndarray,
    period: int,
    input_column: str = "close"
) -> IndicatorResult:
    """
    Running Moving Average (RMA) / Wilder's Smoothing - Pure NumPy float64 Implementation.
    """
    if not isinstance(values, np.ndarray):
        values = np.asarray(values, dtype=np.float64)
    
    n = len(values)
    out = np.full(n, np.nan, dtype=np.float64)
    valid_mask = np.zeros(n, dtype=bool)
    
    if n < period:
        return _build_empty_result(values, timestamps, period, input_column, "Insufficient data")
        
    alpha = 1.0 / period
    
    # Find first non-NaN index
    start_idx = 0
    while start_idx < n and np.isnan(values[start_idx]):
        start_idx += 1
        
    if n - start_idx < period:
        return _build_empty_result(values, timestamps, period, input_column, "Insufficient non-NaN data")
        
    # The first RMA value is the SMA of the first 'period' elements
    first_rma = np.mean(values[start_idx:start_idx+period])
    out[start_idx+period-1] = first_rma
    valid_mask[start_idx+period-1] = True
    
    # We must start the loop exactly at `start_idx + period`
    # We can use the same EMA loop in the backend
    if start_idx + period < n:
        # Note: the ema_loop usually starts from start_idx+1 assuming out[start_idx] is seeded.
        # Since we seeded at start_idx+period-1, we call the loop from that index.
        get_backend().ema_loop(values, out, valid_mask, start_idx + period - 1, alpha)
            
    # strict TA-Lib requires a warmup of `period - 1` before it's considered "valid".
    valid_mask[:start_idx + period - 1] = False
            
    return IndicatorResult(
        values=out,
        timestamps=timestamps,
        valid_mask=valid_mask,
        warmup_period=period - 1,
        lookback=period,
        input_columns=[input_column],
        parameters={"period": period, "alpha": alpha},
        metadata={
            "name": "Running Moving Average",
            "short_name": "RMA",
            "formula": "RMA_t = Value_t * alpha + RMA_{t-1} * (1 - alpha)",
            "references": ["Wilder's Smoothing"],
            "inputs": [input_column],
            "output": ["rma_values"],
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

def _build_empty_result(values: np.ndarray, timestamps: np.ndarray, period: int, col: str, reason: str) -> IndicatorResult:
    return IndicatorResult(
        values=np.full(len(values), np.nan, dtype=np.float64),
        timestamps=timestamps,
        valid_mask=np.zeros(len(values), dtype=bool),
        warmup_period=period - 1,
        lookback=period,
        input_columns=[col],
        parameters={"period": period},
        metadata={"name": "RMA"},
        complexity="O(n)",
        memory_complexity="O(n)",
        version="1.0.0",
        warnings=[reason],
        statistics={"nan_count": len(values), "valid_count": 0}
    )
