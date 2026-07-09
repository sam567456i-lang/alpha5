from dataclasses import dataclass
from enum import Enum
from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO

class RegionRelationshipType(Enum):
    OVERLAPS = "OVERLAPS"
    CONTAINS = "CONTAINS"
    DERIVED_FROM = "DERIVED_FROM"
    SUPERSEDES = "SUPERSEDES"
    INVALIDATES = "INVALIDATES"
    MERGES_WITH = "MERGES_WITH"
    INTERSECTS = "INTERSECTS"
    DOMINANCE_CHANGE = "DOMINANCE_CHANGE"

@dataclass(frozen=True)
class RegionRelationshipDTO(EvidenceDTO):
    """
    Semantic relationship between two regions forming a RegionRelationshipGraph.
    Used for capabilities like Propulsion Blocks or Flip Zones.
    """
    source_region_id: str
    target_region_id: str
    relationship_type: RegionRelationshipType
    
    # Optional metadata detailing the relationship (e.g. overlap area)
    relationship_metadata: dict
