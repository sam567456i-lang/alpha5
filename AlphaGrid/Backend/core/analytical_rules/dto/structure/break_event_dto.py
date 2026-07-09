from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from Backend.core.analytical_rules.dto.event_evidence_dto import EventEvidenceDTO

@dataclass(frozen=True)
class BreakEventDTO(EventEvidenceDTO):
    """
    Standardized DTO for structural breaks, preventing event proliferation.
    Used for internal and external swing breaks.
    """
    break_id: str = ""
    break_type: str = ""
    broken_node: str = ""
    breaking_node: str = ""
    reference_price: float = 0.0
    reference_time: str = ""
    supporting_events: List[str] = field(default_factory=list)
    supporting_states: List[str] = field(default_factory=list)
    confidence_inputs: List[Dict[str, Any]] = field(default_factory=list)
