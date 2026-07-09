from dataclasses import dataclass, field
from typing import List
from enum import Enum
from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO
from Backend.core.analytical_rules.dto.regions.region_identity import RegionIdentityDTO
from Backend.core.analytical_rules.dto.regions.region_geometry import RegionBoundsDTO

class RegionReferenceType(Enum):
    UPPER_BOUND = "UPPER_BOUND"
    LOWER_BOUND = "LOWER_BOUND"
    CENTER = "CENTER"
    PERCENT_25 = "25_PERCENT"
    PERCENT_75 = "75_PERCENT"
    CUSTOM = "CUSTOM"
    FILL_FULL = "FILL_FULL"
    FILL_PARTIAL = "FILL_PARTIAL"

@dataclass(frozen=True)
class RegionDetectedEventDTO(EvidenceDTO):
    """
    Immutable fact that a bounded geometric region exists.
    This replaces specialized events (like ImbalanceDetectedEvent) to unify event hierarchies.
    """
    region_identity: RegionIdentityDTO
    bounds: RegionBoundsDTO
    width: float
    anchor_observation_ids: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class RegionReferenceInteractionEventDTO(EvidenceDTO):
    """
    Immutable fact that price interacted with a mathematical reference inside a region.
    """
    region_identity: RegionIdentityDTO
    reference_type: RegionReferenceType
    interaction_price: float
    interaction_observation_id: str
