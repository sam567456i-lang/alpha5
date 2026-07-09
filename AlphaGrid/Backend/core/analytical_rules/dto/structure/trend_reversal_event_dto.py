from dataclasses import dataclass, field
from typing import List, Dict, Any
from Backend.core.analytical_rules.dto.event_evidence_dto import EventEvidenceDTO

@dataclass(frozen=True)
class TrendReversalEventDTO(EventEvidenceDTO):
    """
    Objective shift in trajectory based on a sequence of internal structural breaks.
    Not a subjective methodology label like CHOCH.
    """
    direction: str = ""
    triggering_break_event_id: str = ""
    affected_nodes: List[str] = field(default_factory=list)
    supporting_evidence: Dict[str, Any] = field(default_factory=dict)
