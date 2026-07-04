import numpy as np
from typing import Any, Dict
from Backend.math.public.indicator_result import IndicatorResult

def calculate_rolling_max(
    values: np.ndarray,
    timestamps: np.ndarray,
    period: int,
    input_column: str = "close"
) -> IndicatorResult:
    if not isinstance(values, np.ndarray):
        values = np.asarray(values, dtype=np.float64)
        
    n = len(values)
    out = np.full(n, np.nan, dtype=np.float64)
    valid_mask = np.zeros(n, dtype=bool)
    
    if n < period:
        return _build_empty_result(values, timestamps, period, input_column, "Insufficient data")
        
    # Standard O(N) rolling max algorithm (using sliding window deque)
    # For NumPy simplicity, we can use stride tricks or sliding_window_view
    # Since numpy > 1.20, np.lib.stride_tricks.sliding_window_view is available
    try:
        from numpy.lib.stride_tricks import sliding_window_view
        windows = sliding_window_view(values, window_shape=period)
        out[period - 1:] = np.nanmax(windows, axis=1)
        valid_mask[period - 1:] = True
    except ImportError:
        # Fallback O(N*K) for older numpy
        for i in range(period - 1, n):
            window = values[i - period + 1 : i + 1]
            out[i] = np.nanmax(window)
            valid_mask[i] = True
            
    # Handle NaN propagation
    for i in range(period - 1, n):
        if np.isnan(values[i]):
            out[i] = np.nan
            
    out[~valid_mask] = np.nan

    return IndicatorResult(
        values=out,
        timestamps=timestamps,
        valid_mask=valid_mask,
        warmup_period=period - 1,
        lookback=period,
        input_columns=[input_column],
        parameters={"period": period},
        metadata={
            "name": "Rolling Maximum",
            "short_name": "ROLL_MAX",
            "inputs": [input_column],
            "output": ["values"],
            "warmup": period - 1,
            "deterministic": True,
            "precision": "exact",
            "complexity": "O(N)",
            "memory": "O(N)",
            "supports_nan": True,
            "supports_inf": True,
            "supports_streaming": False,
            "supports_incremental": False,
        },
        complexity="O(N)",
        memory_complexity="O(N)",
        version="1.0.0",
        warnings=[],
        statistics={
            "nan_count": int(np.sum(np.isnan(out))),
            "valid_count": int(np.sum(valid_mask))
        }
    )

def update_rolling_max(bar: Any, state: Dict[str, Any]) -> Any:
    raise NotImplementedError("Streaming API reserved for future implementation.")

def _build_empty_result(values: np.ndarray, timestamps: np.ndarray, period: int, col: str, reason: str) -> IndicatorResult:
    return IndicatorResult(
        values=np.full(len(values), np.nan, dtype=np.float64),
        timestamps=timestamps,
        valid_mask=np.zeros(len(values), dtype=bool),
        warmup_period=period - 1,
        lookback=period,
        input_columns=[col],
        parameters={"period": period},
        metadata={"name": "Rolling Maximum"},
        complexity="O(n)",
        memory_complexity="O(n)",
        version="1.0.0",
        warnings=[reason],
        statistics={"nan_count": len(values), "valid_count": 0}
    )
