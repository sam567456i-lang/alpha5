import numpy as np
from typing import Any, Dict
from Backend.math.public.indicator_result import IndicatorResult

def calculate_correlation(
    x: np.ndarray,
    y: np.ndarray,
    timestamps: np.ndarray,
    period: int,
    input_columns: list = None
) -> IndicatorResult:
    if input_columns is None:
        input_columns = ["x", "y"]
        
    if not isinstance(x, np.ndarray):
        x = np.asarray(x, dtype=np.float64)
    if not isinstance(y, np.ndarray):
        y = np.asarray(y, dtype=np.float64)
        
    n = len(x)
    out = np.full(n, np.nan, dtype=np.float64)
    valid_mask = np.zeros(n, dtype=bool)
    
    if n < period or len(y) != n:
        return _build_empty_result(x, timestamps, period, input_columns, "Insufficient data or shape mismatch")
        
    try:
        from numpy.lib.stride_tricks import sliding_window_view
        x_win = sliding_window_view(x, window_shape=period)
        y_win = sliding_window_view(y, window_shape=period)
        
        x_mean = np.nanmean(x_win, axis=1, keepdims=True)
        y_mean = np.nanmean(y_win, axis=1, keepdims=True)
        
        x_dev = x_win - x_mean
        y_dev = y_win - y_mean
        
        cov = np.nansum(x_dev * y_dev, axis=1)
        x_var = np.nansum(x_dev**2, axis=1)
        y_var = np.nansum(y_dev**2, axis=1)
        
        # Pearson correlation
        denom = np.sqrt(x_var * y_var)
        corr = np.zeros_like(cov)
        valid_denom = denom != 0
        corr[valid_denom] = cov[valid_denom] / denom[valid_denom]
        
        out[period - 1:] = corr
        valid_mask[period - 1:] = ~np.isnan(corr)
    except ImportError:
        for i in range(period - 1, n):
            xw = x[i - period + 1 : i + 1]
            yw = y[i - period + 1 : i + 1]
            valid = ~(np.isnan(xw) | np.isnan(yw))
            if np.sum(valid) > 1:
                mat = np.corrcoef(xw[valid], yw[valid])
                out[i] = mat[0, 1]
                valid_mask[i] = True

    out[~valid_mask] = np.nan

    return IndicatorResult(
        values=out,
        timestamps=timestamps,
        valid_mask=valid_mask,
        warmup_period=period - 1,
        lookback=period,
        input_columns=input_columns,
        parameters={"period": period},
        metadata={
            "name": "Correlation",
            "short_name": "CORR",
            "inputs": input_columns,
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
        complexity="O(N)",
        memory_complexity="O(N)",
        version="1.0.0",
        warnings=[],
        statistics={
            "nan_count": int(np.sum(np.isnan(out))),
            "valid_count": int(np.sum(valid_mask))
        }
    )

def update_correlation(bar: Any, state: Dict[str, Any]) -> Any:
    raise NotImplementedError("Streaming API reserved for future implementation.")

def _build_empty_result(values: np.ndarray, timestamps: np.ndarray, period: int, cols: list, reason: str) -> IndicatorResult:
    return IndicatorResult(
        values=np.full(len(values), np.nan, dtype=np.float64),
        timestamps=timestamps,
        valid_mask=np.zeros(len(values), dtype=bool),
        warmup_period=period - 1,
        lookback=period,
        input_columns=cols,
        parameters={"period": period},
        metadata={"name": "Correlation"},
        complexity="O(n)",
        memory_complexity="O(n)",
        version="1.0.0",
        warnings=[reason],
        statistics={"nan_count": len(values), "valid_count": 0}
    )
