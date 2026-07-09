from dataclasses import dataclass, field
from typing import List, Dict, Any
from Backend.core.analytical_rules.dto.state_evidence_dto import StateEvidenceDTO

@dataclass(frozen=True)
class EqualHighState(StateEvidenceDTO):
    """
    State representing identified equal highs.
    """
    anchor_ids: List[str] = field(default_factory=list)
    anchor_count: int = 0
    average_price: float = 0.0
    price_variance: float = 0.0

@dataclass(frozen=True)
class EqualLowState(StateEvidenceDTO):
    """
    State representing identified equal lows.
    """
    anchor_ids: List[str] = field(default_factory=list)
    anchor_count: int = 0
    average_price: float = 0.0
    price_variance: float = 0.0
