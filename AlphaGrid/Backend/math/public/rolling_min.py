import numpy as np
from typing import Any, Dict
from Backend.math.public.indicator_result import IndicatorResult

def calculate_rolling_min(
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
        
    try:
        from numpy.lib.stride_tricks import sliding_window_view
        windows = sliding_window_view(values, window_shape=period)
        out[period - 1:] = np.nanmin(windows, axis=1)
        valid_mask[period - 1:] = True
    except ImportError:
        for i in range(period - 1, n):
            window = values[i - period + 1 : i + 1]
            out[i] = np.nanmin(window)
            valid_mask[i] = True
            
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
            "name": "Rolling Minimum",
            "short_name": "ROLL_MIN",
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

def update_rolling_min(bar: Any, state: Dict[str, Any]) -> Any:
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
        metadata={"name": "Rolling Minimum"},
        complexity="O(n)",
        memory_complexity="O(n)",
        version="1.0.0",
        warnings=[reason],
        statistics={"nan_count": len(values), "valid_count": 0}
    )
