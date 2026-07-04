import numpy as np
from typing import Any, Dict
from Backend.math.public.indicator_result import IndicatorResult

def calculate_vwap(
    typical_price: np.ndarray,
    volume: np.ndarray,
    timestamps: np.ndarray,
    input_column: str = "close"
) -> IndicatorResult:
    """
    Volume Weighted Average Price (VWAP) - Cumulative over the provided arrays.
    """
    if not isinstance(typical_price, np.ndarray):
        typical_price = np.asarray(typical_price, dtype=np.float64)
    if not isinstance(volume, np.ndarray):
        volume = np.asarray(volume, dtype=np.float64)
        
    n = len(typical_price)
    out = np.full(n, np.nan, dtype=np.float64)
    valid_mask = np.zeros(n, dtype=bool)
    
    if n == 0:
        return _build_empty_result(typical_price, timestamps, input_column, "Empty array")
        
    pv = typical_price * volume
    
    # Cumulative sum
    cum_pv = np.nancumsum(pv)
    cum_vol = np.nancumsum(volume)
    
    with np.errstate(invalid='ignore', divide='ignore'):
        out = cum_pv / cum_vol
        
    # Valid where volume > 0 and typical_price is not nan
    valid_mask = ~np.isnan(out) & (cum_vol > 0)
    out[~valid_mask] = np.nan

    return IndicatorResult(
        values=out,
        timestamps=timestamps,
        valid_mask=valid_mask,
        warmup_period=0,
        lookback=1,
        input_columns=[input_column],
        parameters={},
        metadata={
            "name": "Volume Weighted Average Price",
            "short_name": "VWAP",
            "formula": "sum(Price * Volume) / sum(Volume)",
            "inputs": [input_column],
            "output": ["vwap"],
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

def _build_empty_result(values: np.ndarray, timestamps: np.ndarray, col: str, reason: str) -> IndicatorResult:
    return IndicatorResult(
        values=np.full(len(values), np.nan, dtype=np.float64),
        timestamps=timestamps,
        valid_mask=np.zeros(len(values), dtype=bool),
        warmup_period=0,
        lookback=1,
        input_columns=[col],
        parameters={},
        metadata={"name": "VWAP"},
        complexity="O(n)",
        memory_complexity="O(n)",
        version="1.0.0",
        warnings=[reason],
        statistics={"nan_count": len(values), "valid_count": 0}
    )
