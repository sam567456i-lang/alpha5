from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class ConfidenceProfileDTO:
    raw_confidence: float
    adjusted_confidence: float
    confidence_sources: List[str]
    penalties: List[str]
    boosts: List[str]
    uncertainty_factor: float
