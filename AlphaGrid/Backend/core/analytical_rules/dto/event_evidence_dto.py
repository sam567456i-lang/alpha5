from dataclasses import dataclass
from typing import List, Dict, Any
from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO

@dataclass(frozen=True)
class EventEvidenceDTO(EvidenceDTO):
    """Represents instantaneous analytical occurrences affecting market state."""
    event_id: str
    event_timestamp: str
    trigger_rule: str
    trigger_evidence: str
    affected_state_ids: List[str]
    causal_events: List[Dict[str, Any]]
    severity: str
    sequence_number: int
    confidence_inputs: List[str]
