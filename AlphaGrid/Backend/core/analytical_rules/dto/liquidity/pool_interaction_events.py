from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from Backend.core.analytical_rules.dto.event_evidence_dto import EventEvidenceDTO

class PoolInteractionType(Enum):
    APPROACH = "APPROACH"
    TOUCH = "TOUCH"
    ENTER = "ENTER"
    EXIT = "EXIT"
    PENETRATE = "PENETRATE"
    REJECT = "REJECT"
    COMPLETE_TRAVERSAL = "COMPLETE_TRAVERSAL"

@dataclass(frozen=True)
class PoolInteractionEventDTO(EventEvidenceDTO):
    """
    Generic DTO representing the objective historical fact that a geometric interaction occurred.
    """
    pool_id: str = ""
    interaction_type: PoolInteractionType = PoolInteractionType.TOUCH
    observation_id: str = ""
    
    # Rich Event Geometry
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
    maximum_penetration: float = 0.0
    duration: int = 1
    interaction_path: str = ""
    observed_price_reference: str = ""
