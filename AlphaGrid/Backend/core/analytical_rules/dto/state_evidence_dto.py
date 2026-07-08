from dataclasses import dataclass
from typing import List
from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO

@dataclass(frozen=True)
class StateEvidenceDTO(EvidenceDTO):
    """Represents persistent analytical entities with lifecycles and relationships."""
    state_id: str
    created_at: str
    valid_from: str
    valid_until: str
    is_active: bool
    invalidated_at: str
    invalidated_by: str
    superseded_by: str
    related_state_ids: List[str]
    related_event_ids: List[str]
    confidence_inputs: List[str]
