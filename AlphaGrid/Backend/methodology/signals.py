"""Rich Trading Signals."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class Signal:
    """
    Rich signal object produced by a Methodology.
    """
    direction: str  # e.g., 'LONG', 'SHORT', 'WAIT'
    confidence: float
    strength: float
    reason: str
    concept_ids: List[str]
    methodology: str
    provider: Optional[str] = field(default=None)
