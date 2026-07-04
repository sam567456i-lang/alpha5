import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass(frozen=True)
class IndicatorResult:
    """
    Standardized primitive output for the Mathematical Core Layer.
    Once this file is frozen in Phase 10g, any changes require an RFC.
    """
    values: np.ndarray
    timestamps: np.ndarray
    valid_mask: np.ndarray
    warmup_period: int
    lookback: int
    input_columns: List[str]
    parameters: Dict[str, Any]
    metadata: Dict[str, Any]
    complexity: str
    memory_complexity: str
    version: str
    warnings: List[str] = field(default_factory=list)
    statistics: Dict[str, Any] = field(default_factory=dict)
