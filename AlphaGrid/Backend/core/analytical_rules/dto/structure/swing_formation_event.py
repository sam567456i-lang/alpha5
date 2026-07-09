from dataclasses import dataclass
from Backend.core.analytical_rules.dto.event_evidence_dto import EventEvidenceDTO

from Backend.core.analytical_rules.dto.structure.swing_identity_dto import SwingIdentityDTO

@dataclass(frozen=True)
class SwingFormationEvent(EventEvidenceDTO):
    """
    Emitted when a geometric swing is confirmed by the SwingDetector.
    Contains raw geometric facts, stripped of subjective terminology.
    """
    swing: SwingIdentityDTO
