"""Methodology Evaluation Data Structure."""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass(frozen=True)
class MethodologyEvaluation:
    """
    Represents the output of a Methodology.
    Captures the semantic interpretation of the market before it is converted into a trade intent (Signal).
    """
    methodology_id: str
    timestamp: Optional[datetime]
    is_active: bool
    direction: int  # 1 for bullish, -1 for bearish, 0 for neutral
    confidence: float
    supporting_concepts: Dict[str, int] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
