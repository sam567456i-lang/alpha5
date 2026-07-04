import numpy as np
from typing import Any, Dict
from Backend.math.public.indicator_result import IndicatorResult

def calculate_shift(
    values: np.ndarray,
    timestamps: np.ndarray,
    period: int = 1,
    input_column: str = "close"
) -> IndicatorResult:
    """
    Shifts the array backward by `period` steps (like pandas shift).
    """
    if not isinstance(values, np.ndarray):
        values = np.asarray(values, dtype=np.float64)
        
    n = len(values)
    out = np.full(n, np.nan, dtype=np.float64)
    valid_mask = np.zeros(n, dtype=bool)
    
    if n <= period:
        return _build_empty_result(values, timestamps, period, input_column, "Insufficient data")
        
    out[period:] = values[:-period]
    valid_mask[period:] = ~np.isnan(out[period:])
    
    out[~valid_mask] = np.nan

    return IndicatorResult(
        values=out,
        timestamps=timestamps,
        valid_mask=valid_mask,
        warmup_period=period,
        lookback=period,
        input_columns=[input_column],
        parameters={"period": period},
        metadata={
            "name": "Shift",
            "short_name": "SHIFT",
            "inputs": [input_column],
            "output": ["values"],
            "warmup": period,
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

def update_shift(bar: Any, state: Dict[str, Any]) -> Any:
    raise NotImplementedError("Streaming API reserved for future implementation.")

def _build_empty_result(values: np.ndarray, timestamps: np.ndarray, period: int, col: str, reason: str) -> IndicatorResult:
    return IndicatorResult(
        values=np.full(len(values), np.nan, dtype=np.float64),
        timestamps=timestamps,
        valid_mask=np.zeros(len(values), dtype=bool),
        warmup_period=period,
        lookback=period,
        input_columns=[col],
        parameters={"period": period},
        metadata={"name": "Shift"},
        complexity="O(n)",
        memory_complexity="O(n)",
        version="1.0.0",
        warnings=[reason],
        statistics={"nan_count": len(values), "valid_count": 0}
    )
