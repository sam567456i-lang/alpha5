import numpy as np
from typing import Any, Dict
from Backend.math.public.indicator_result import IndicatorResult
from Backend.math.public.ema import _build_empty_result

def calculate_variance(
    values: np.ndarray,
    timestamps: np.ndarray,
    period: int,
    input_column: str = "close",
    ddof: int = 1
) -> IndicatorResult:
    """
    Rolling Variance - Pure NumPy float64 Implementation.
    """
    if not isinstance(values, np.ndarray):
        values = np.asarray(values, dtype=np.float64)
        
    n = len(values)
    out = np.full(n, np.nan, dtype=np.float64)
    valid_mask = np.zeros(n, dtype=bool)
    
    if n < period:
        return _build_empty_result(values, timestamps, period, input_column, "Insufficient data")
        
    # We use numpy stride tricks or a simple loop for safety against NaNs
    for i in range(period - 1, n):
        window = values[i - period + 1: i + 1]
        if not np.isnan(window).any():
            out[i] = np.var(window, ddof=ddof)
            valid_mask[i] = True
            
    return IndicatorResult(
        values=out,
        timestamps=timestamps,
        valid_mask=valid_mask,
        warmup_period=period - 1,
        lookback=period,
        input_columns=[input_column],
        parameters={"period": period, "ddof": ddof},
        metadata={
            "name": "Rolling Variance",
            "short_name": "VAR",
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


def update_variance(bar: Any, state: Dict[str, Any]) -> Any:
    raise NotImplementedError("Streaming API reserved for future implementation.")
