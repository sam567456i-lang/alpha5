from dataclasses import dataclass
import numpy as np
from typing import Dict, Any, List

@dataclass(frozen=True)
class FinancialIndicatorResult:
    """Base class for all indicator engine results. Purely numerical."""
    timestamps: np.ndarray
    valid_mask: np.ndarray
    warmup_period: int
    lookback: int
    metadata: Dict[str, Any]
    
@dataclass(frozen=True)
class MACDResult(FinancialIndicatorResult):
    macd: np.ndarray
    signal: np.ndarray
    histogram: np.ndarray

@dataclass(frozen=True)
class ROCResult(FinancialIndicatorResult):
    roc: np.ndarray
