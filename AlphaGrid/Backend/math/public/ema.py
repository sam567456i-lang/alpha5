import numpy as np
import time
from typing import Dict, Any
from Backend.math.public.indicator_result import IndicatorResult

def calculate_ema(
    values: np.ndarray,
    timestamps: np.ndarray,
    period: int,
    input_column: str = "close"
) -> IndicatorResult:
    """
    Exponential Moving Average (EMA) - Pure NumPy float64 Implementation.
    """
    if not isinstance(values, np.ndarray):
        values = np.asarray(values, dtype=np.float64)
    
    n = len(values)
    out = np.full(n, np.nan, dtype=np.float64)
    valid_mask = np.zeros(n, dtype=bool)
    
    if n < period:
        return _build_empty_result(values, timestamps, period, input_column, "Insufficient data")
        
    alpha = 2.0 / (period + 1.0)
    
    # Find first non-NaN index
    start_idx = 0
    while start_idx < n and np.isnan(values[start_idx]):
        start_idx += 1
        
    if n - start_idx < period:
        return _build_empty_result(values, timestamps, period, input_column, "Insufficient non-NaN data")
        
    # The first EMA value is the SMA of the first 'period' elements
    first_ema = np.mean(values[start_idx:start_idx+period])
    out[start_idx+period-1] = first_ema
    valid_mask[start_idx+period-1] = True
    
    # We could also use the first value as seed (like adjust=False in Pandas), 
    # but the canonical SMA seed is mathematically purer for MACD in institutional contexts.
    # Actually, Pandas `ewm(adjust=False)` uses the first value directly. We will use the 
    # first value to match Pandas-TA / TA-Lib `adjust=False` exactly.
    out[start_idx] = values[start_idx]
    valid_mask[start_idx] = True
    
    prev_ema = out[start_idx]
    
    from Backend.math.internal.kernels import ema_loop
    ema_loop(values, out, valid_mask, start_idx, alpha)
            
    # However, strict TA-Lib requires a warmup of `period - 1` before it's considered "valid".
    # We will enforce valid_mask strictly but NOT null out the values to allow downstream generators
    # (like MACD's signal line) to seed identically to Pandas ewm(min_periods=0).
    valid_mask[:start_idx + period - 1] = False
    
    # We DO NOT set out[~valid_mask] = np.nan because it breaks recursive indicators.
            
    return IndicatorResult(
        values=out,
        timestamps=timestamps,
        valid_mask=valid_mask,
        warmup_period=period - 1,
        lookback=period,
        input_columns=[input_column],
        parameters={"period": period, "alpha": alpha},
        metadata={
            "name": "Exponential Moving Average",
            "short_name": "EMA",
            "formula": "EMA_t = Value_t * alpha + EMA_{t-1} * (1 - alpha)",
            "references": ["TA-Lib EMA", "Pandas EWM (adjust=False)"],
            "inputs": [input_column],
            "output": ["ema_values"],
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

def update_ema(bar: Any, state: Dict[str, Any]) -> Any:
    """
    Reserved streaming API for live execution.
    """
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
        metadata={"name": "EMA"},
        complexity="O(n)",
        memory_complexity="O(n)",
        version="1.0.0",
        warnings=[reason],
        statistics={"nan_count": len(values), "valid_count": 0}
    )
