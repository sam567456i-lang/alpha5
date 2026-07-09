from dataclasses import dataclass
from typing import Any
from Backend.core.analytical_rules.dto.structure.structure_state import StructureState
from Backend.core.analytical_rules.dto.event_evidence_dto import EventEvidenceDTO

from Backend.core.analytical_rules.dto.structure.structure_transition_reason import StructureTransitionReason
from Backend.core.analytical_rules.dto.structure.structure_transition_type import StructureTransitionType

@dataclass(frozen=True)
class StructureTransition:
    """
    Explicit transition object capturing a state delta for causality tracking and replay.
    """
    old_state: StructureState
    event: EventEvidenceDTO
    new_state: StructureState
    transition_id: str
    timestamp: str
    transition_type: StructureTransitionType
    transition_reason: StructureTransitionReason
