import numpy as np
from typing import Any, Dict
from Backend.math.public.indicator_result import IndicatorResult

def calculate_covariance(
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
        
    # O(N) rolling covariance using sliding windows
    try:
        from numpy.lib.stride_tricks import sliding_window_view
        x_win = sliding_window_view(x, window_shape=period)
        y_win = sliding_window_view(y, window_shape=period)
        
        # Calculate means
        x_mean = np.nanmean(x_win, axis=1, keepdims=True)
        y_mean = np.nanmean(y_win, axis=1, keepdims=True)
        
        # Calculate covariance (ddof=1)
        cov = np.nansum((x_win - x_mean) * (y_win - y_mean), axis=1) / (period - 1)
        out[period - 1:] = cov
        valid_mask[period - 1:] = ~np.isnan(cov)
    except ImportError:
        for i in range(period - 1, n):
            xw = x[i - period + 1 : i + 1]
            yw = y[i - period + 1 : i + 1]
            valid = ~(np.isnan(xw) | np.isnan(yw))
            if np.sum(valid) > 1:
                cov_mat = np.cov(xw[valid], yw[valid], ddof=1)
                out[i] = cov_mat[0, 1]
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
            "name": "Covariance",
            "short_name": "COV",
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

def update_covariance(bar: Any, state: Dict[str, Any]) -> Any:
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
        metadata={"name": "Covariance"},
        complexity="O(n)",
        memory_complexity="O(n)",
        version="1.0.0",
        warnings=[reason],
        statistics={"nan_count": len(values), "valid_count": 0}
    )
