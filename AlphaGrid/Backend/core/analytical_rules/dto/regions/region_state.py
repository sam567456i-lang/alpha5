from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any

from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus
from Backend.core.analytical_rules.dto.regions.region_identity import RegionIdentityDTO
from Backend.core.analytical_rules.dto.regions.region_geometry import RegionGeometryDTO

class RegionLifecycleState(Enum):
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FULLY_FILLED = "FULLY_FILLED"
    SUPERSEDED = "SUPERSEDED"
    MERGED = "MERGED"
    INVALIDATED = "INVALIDATED"
    ARCHIVED = "ARCHIVED"

from Backend.core.analytical_rules.dto.regions.region_metadata import RegionMetadataDTO

@dataclass
class RegionState:
    """
    Unified mutable projection for any bounded region (FVG, Order Block, Breaker, etc.).
    Replaces capability-specific states like ImbalanceState.
    """
    identity: EvidenceIdentityDTO
    metadata: EvidenceMetadataDTO
    provenance: EvidenceProvenanceDTO
    classification: EvidenceClassification
    interpretation_level: InterpretationLevel
    validity_status: ValidityStatus
    evidence_data: dict
    
    region_identity: RegionIdentityDTO
    geometry: RegionGeometryDTO
    lifecycle_state: RegionLifecycleState
    remaining_height: float
    
    region_metadata: RegionMetadataDTO = field(default_factory=RegionMetadataDTO)
