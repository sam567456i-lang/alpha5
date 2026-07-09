from dataclasses import dataclass, field
from typing import List
from Backend.core.analytical_rules.dto.event_evidence_dto import EventEvidenceDTO

@dataclass(frozen=True)
class EqualHighDetectedEventDTO(EventEvidenceDTO):
    """
    Event emitted when a cluster of anchors meets the criteria for Equal Highs.
    """
    anchor_ids: List[str] = field(default_factory=list)
    anchor_count: int = 0
    average_price: float = 0.0
    price_variance: float = 0.0

@dataclass(frozen=True)
class EqualLowDetectedEventDTO(EventEvidenceDTO):
    """
    Event emitted when a cluster of anchors meets the criteria for Equal Lows.
    """
    anchor_ids: List[str] = field(default_factory=list)
    anchor_count: int = 0
    average_price: float = 0.0
    price_variance: float = 0.0
