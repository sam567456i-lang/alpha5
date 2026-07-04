import numpy as np
from typing import Any, Dict
from Backend.math.public.indicator_result import IndicatorResult
from Backend.math.public.ema import _build_empty_result

def calculate_wma(
    values: np.ndarray,
    timestamps: np.ndarray,
    period: int,
    input_column: str = "close"
) -> IndicatorResult:
    """
    Weighted Moving Average (WMA) - Pure NumPy float64 Implementation.
    """
    if not isinstance(values, np.ndarray):
        values = np.asarray(values, dtype=np.float64)
        
    n = len(values)
    out = np.full(n, np.nan, dtype=np.float64)
    valid_mask = np.zeros(n, dtype=bool)
    
    if n < period:
        return _build_empty_result(values, timestamps, period, input_column, "Insufficient data")
        
    weights = np.arange(1, period + 1, dtype=np.float64)
    weight_sum = np.sum(weights)
    
    # We use stride tricks for a vectorized sliding window dot product
    # Ensure no NaNs exist in the window
    for i in range(period - 1, n):
        window = values[i - period + 1: i + 1]
        if not np.isnan(window).any():
            out[i] = np.dot(window, weights) / weight_sum
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
            "name": "Weighted Moving Average",
            "short_name": "WMA",
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
        complexity="O(n * period)",
        memory_complexity="O(n)",
        version="1.0.0",
        warnings=[],
        statistics={
            "nan_count": int(np.sum(np.isnan(out))),
            "valid_count": int(np.sum(valid_mask))
        }
    )


def update_wma(bar: Any, state: Dict[str, Any]) -> Any:
    raise NotImplementedError("Streaming API reserved for future implementation.")
