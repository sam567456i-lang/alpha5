# Strict Public API Exports for the Math Core
# Feature generators must ONLY import from this module.

from Backend.math.public.ema import calculate_ema, update_ema
from Backend.math.public.sma import calculate_sma, update_sma
from Backend.math.public.wma import calculate_wma, update_wma
from Backend.math.public.rolling_sum import calculate_rolling_sum, update_rolling_sum
from Backend.math.public.rolling_max import calculate_rolling_max, update_rolling_max
from Backend.math.public.rolling_min import calculate_rolling_min, update_rolling_min
from Backend.math.public.diff import calculate_diff, update_diff
from Backend.math.public.shift import calculate_shift, update_shift
from Backend.math.public.clip import calculate_clip, update_clip
from Backend.math.public.variance import calculate_variance, update_variance
from Backend.math.public.stddev import calculate_stddev, update_stddev
from Backend.math.public.covariance import calculate_covariance, update_covariance
from Backend.math.public.correlation import calculate_correlation, update_correlation
from Backend.math.public.roc import calculate_roc, update_roc
from Backend.math.public.indicator_result import IndicatorResult

__all__ = [
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
]
