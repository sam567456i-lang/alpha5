import numpy as np
from typing import Any, Dict
from Backend.math.public.indicator_result import IndicatorResult
from Backend.math.public.ema import _build_empty_result
from Backend.math.public.variance import calculate_variance

def calculate_stddev(
    values: np.ndarray,
    timestamps: np.ndarray,
    period: int,
    input_column: str = "close",
    ddof: int = 1
) -> IndicatorResult:
    """
    Rolling Standard Deviation - Pure NumPy float64 Implementation.
    """
    var_result = calculate_variance(values, timestamps, period, input_column, ddof)
    
    # We can just take the sqrt of the variance values
    out = np.sqrt(var_result.values)
    
    return IndicatorResult(
        values=out,
        timestamps=var_result.timestamps,
        valid_mask=var_result.valid_mask,
        warmup_period=var_result.warmup_period,
        lookback=var_result.lookback,
        input_columns=[input_column],
        parameters={"period": period, "ddof": ddof},
        metadata={
            "name": "Rolling Standard Deviation",
            "short_name": "STDDEV",
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
            "valid_count": int(np.sum(var_result.valid_mask))
        }
    )


def update_stddev(bar: Any, state: Dict[str, Any]) -> Any:
    raise NotImplementedError("Streaming API reserved for future implementation.")
