import numpy as np
from typing import Any, Dict
from Backend.math.public.indicator_result import IndicatorResult

def calculate_clip(
    values: np.ndarray,
    timestamps: np.ndarray,
    lower: float = None,
    upper: float = None,
    input_column: str = "close"
) -> IndicatorResult:
    """
    Clips values between a lower and upper bound.
    """
    if not isinstance(values, np.ndarray):
        values = np.asarray(values, dtype=np.float64)
        
    n = len(values)
    out = np.copy(values)
    valid_mask = ~np.isnan(values)
    
    if lower is not None:
        out = np.where(out < lower, lower, out)
    if upper is not None:
        out = np.where(out > upper, upper, out)
        
    out[~valid_mask] = np.nan

    return IndicatorResult(
        values=out,
        timestamps=timestamps,
        valid_mask=valid_mask,
        warmup_period=0,
        lookback=1,
        input_columns=[input_column],
        parameters={"lower": lower, "upper": upper},
        metadata={
            "name": "Clip",
            "short_name": "CLIP",
            "inputs": [input_column],
            "output": ["values"],
            "warmup": 0,
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

def update_clip(bar: Any, state: Dict[str, Any]) -> Any:
    raise NotImplementedError("Streaming API reserved for future implementation.")
