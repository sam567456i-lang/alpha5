from dataclasses import dataclass, field
from typing import List, Dict, Any
from Backend.core.analytical_rules.dto.event_evidence_dto import EventEvidenceDTO

@dataclass(frozen=True)
class StructuralShiftEventDTO(EventEvidenceDTO):
    """
    Larger scale, confirmed transition. 
    Consumes TrendReversalEvents and historical breaks.
    """
    direction: str = ""
    triggering_reversal_event_id: str = ""
    affected_nodes: List[str] = field(default_factory=list)
    supporting_evidence: Dict[str, Any] = field(default_factory=dict)
