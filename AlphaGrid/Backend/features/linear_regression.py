"""Linear Regression Feature."""
from typing import Any, Dict, List, Optional
import math
from Shared.models.market import MarketSnapshot
from .base import AbstractFeature

class LinRegFeature(AbstractFeature):
    """
    Computes a Linear Regression (Least Squares) moving average over a specified period.
    Formula: y = mx + b, where x is time and y is price.
    Returns the ending point of the regression line (the current value).
    """
    
    def __init__(self, period: int = 20) -> None:
        self.period = period
        self._window: List[float] = []

    @classmethod
    def get_name(cls) -> str:
        return "LinReg_20"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        return []

    @classmethod
    def warmup_period(cls) -> int:
        return 20

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Optional[float]:
        price = float(snapshot.close)
        self._window.append(price)
        
        if len(self._window) > self.period:
            self._window.pop(0)
            
        if len(self._window) < self.period:
            return None
            
        # Compute least squares
        n = self.period
        sum_x = n * (n + 1) / 2.0
        sum_y = sum(self._window)
        sum_x_sq = n * (n + 1) * (2 * n + 1) / 6.0
        sum_xy = sum((i + 1) * y for i, y in enumerate(self._window))
        
        denominator = (n * sum_x_sq - sum_x * sum_x)
        if denominator == 0:
            return sum_y / n
            
        m = (n * sum_xy - sum_x * sum_y) / denominator
        b = (sum_y - m * sum_x) / n
        
        # We want the value at the current point (x = n)
        return m * n + b
