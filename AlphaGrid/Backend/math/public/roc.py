import numpy as np
from typing import Any, Dict
from Backend.math.public.indicator_result import IndicatorResult
from Backend.math.public.ema import _build_empty_result

def calculate_roc(
    values: np.ndarray,
    timestamps: np.ndarray,
    period: int,
    input_column: str = "close"
) -> IndicatorResult:
    """
    Rate of Change (ROC) - Pure NumPy float64 Implementation.
    """
    if not isinstance(values, np.ndarray):
        values = np.asarray(values, dtype=np.float64)
        
    n = len(values)
    out = np.full(n, np.nan, dtype=np.float64)
    valid_mask = np.zeros(n, dtype=bool)
    
    if n < period + 1:
        return _build_empty_result(values, timestamps, period + 1, input_column, "Insufficient data")
        
    # Vectorized ROC calculation
    # Formula: ((current - previous) / previous) * 100
    # To handle 0.0 division natively in numpy without crashing, we suppress the warning
    # and allow np.inf to be produced, matching legacy pandas behavior.
    with np.errstate(divide='ignore', invalid='ignore'):
        roc_values = ((values[period:] - values[:-period]) / values[:-period]) * 100.0
        
    out[period:] = roc_values
    
    # Generate valid mask. NaN values propagate validity as False.
    valid_mask[period:] = ~np.isnan(roc_values)
    
    return IndicatorResult(
        values=out,
        timestamps=timestamps,
        valid_mask=valid_mask,
        warmup_period=period,
        lookback=period + 1,
        input_columns=[input_column],
        parameters={"period": period},
        metadata={
            "name": "Rate of Change",
            "short_name": "ROC",
            "inputs": [input_column],
            "output": ["roc_values"],
            "warmup": period,
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

def update_roc(bar: Any, state: Dict[str, Any]) -> Any:
    raise NotImplementedError("Streaming API reserved for future implementation.")
