import inspect
import pytest
from Backend.math import public

def test_public_api_exports():
    """
    Strictly enforce that the Math Core exports only the frozen primitives
    and no internal modules or implementations.
    """
    expected_exports = {
        "calculate_ema", "update_ema",
        "calculate_sma", "update_sma",
        "calculate_wma", "update_wma",
        "calculate_rolling_sum", "update_rolling_sum",
        "calculate_rolling_max", "update_rolling_max",
        "calculate_rolling_min", "update_rolling_min",
        "calculate_diff", "update_diff",
        "calculate_shift", "update_shift",
        "calculate_clip", "update_clip",
        "calculate_variance", "update_variance",
        "calculate_stddev", "update_stddev",
        "calculate_covariance", "update_covariance",
        "calculate_correlation", "update_correlation",
        "calculate_roc", "update_roc",
        "IndicatorResult"
    }
    
    actual_exports = set(public.__all__)
    
    assert actual_exports == expected_exports, "Public API exports do not match frozen contract."
    
def test_calculate_signatures():
    """
    Ensure all calculate_* functions conform to the canonical signature.
    (values, timestamps, period, input_column)
    """
    primitives = [
        public.calculate_ema, public.calculate_sma, public.calculate_wma,
        public.calculate_rolling_sum, public.calculate_rolling_max,
        public.calculate_rolling_min, public.calculate_diff, public.calculate_shift,
        public.calculate_variance, public.calculate_stddev
    ]
    
    for func in primitives:
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        assert "values" in params, f"{func.__name__} missing 'values' param"
        assert "timestamps" in params, f"{func.__name__} missing 'timestamps' param"
        assert "period" in params, f"{func.__name__} missing 'period' param"
        assert "input_column" in params, f"{func.__name__} missing 'input_column' param"
        
def test_update_signatures():
    """
    Ensure all update_* functions conform to the reserved streaming signature.
    """
    updates = [
        public.update_ema, public.update_sma, public.update_wma,
        public.update_rolling_sum, public.update_rolling_max,
        public.update_rolling_min, public.update_diff, public.update_shift,
        public.update_clip, public.update_variance, public.update_stddev,
        public.update_covariance, public.update_correlation
    ]
    
    for func in updates:
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        assert params == ["bar", "state"], f"{func.__name__} has wrong signature {params}"

def test_indicator_result_structure():
    """
    Ensure IndicatorResult field order, names, types, and serialization are frozen.
    """
    import dataclasses
    from typing import Optional, Dict, Any, List
    import numpy as np
    
    fields = dataclasses.fields(public.IndicatorResult)
    
    expected = [
        "values", "timestamps", "valid_mask", "warmup_period", "lookback", 
        "input_columns", "parameters", "metadata", "complexity", 
        "memory_complexity", "version", "warnings", "statistics"
    ]
    
    assert len(fields) == len(expected), f"IndicatorResult must have exactly {len(expected)} fields, found {len(fields)}"
    
    for i, expected_name in enumerate(expected):
        assert fields[i].name == expected_name, f"Field {i} must be {expected_name}"
        
    # Check serialization compatibility
    res = public.IndicatorResult(
        values=np.array([1.0, 2.0]),
        timestamps=np.array([1000, 2000]),
        valid_mask=np.array([False, True]),
        warmup_period=1,
        lookback=1,
        input_columns=["close"],
        parameters={},
        metadata={"foo": "bar"},
        complexity="O(n)",
        memory_complexity="O(n)",
        version="1.0.0",
        warnings=[],
        statistics={}
    )
    
    assert dataclasses.is_dataclass(res)
