import uuid
from typing import Optional

from Backend.core.analytical_rules.dto.regions.region_events import RegionDetectedEventDTO
from Backend.core.analytical_rules.dto.regions.region_identity import RegionIdentityDTO, RegionType
from Backend.core.analytical_rules.dto.regions.region_geometry import RegionBoundsDTO
from Backend.core.analytical_rules.dto.regions.region_state import RegionState
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class BPRRule:
    """
    Derived rule that creates a Balanced Price Range (BPR) region
    when two FVG regions overlap. Strictly consumes certified state evidence.
    """
    
    def evaluate(self, fvg_a: RegionState, fvg_b: RegionState) -> Optional[RegionDetectedEventDTO]:
        if fvg_a.region_identity.region_type != RegionType.FVG or fvg_b.region_identity.region_type != RegionType.FVG:
            return None
            
        # Calculate overlap
        upper_overlap = min(fvg_a.geometry.bounds.upper_bound, fvg_b.geometry.bounds.upper_bound)
        lower_overlap = max(fvg_a.geometry.bounds.lower_bound, fvg_b.geometry.bounds.lower_bound)
        
        # If no overlap
        if upper_overlap <= lower_overlap:
            return None
            
        event_id = f"BPR-DETECTED-{uuid.uuid4()}"
        region_id = f"REGION-BPR-{uuid.uuid4()}"
        
        region_identity = RegionIdentityDTO(
            region_id=region_id,
            region_type=RegionType.BPR,
            anchor_ids=[fvg_a.identity.evidence_id, fvg_b.identity.evidence_id],
            graph_namespace="regions/bpr",
            policy_checksum="none",
            geometry_fingerprint=f"{lower_overlap}-{upper_overlap}"
        )
        
        bounds = RegionBoundsDTO(upper_bound=upper_overlap, lower_bound=lower_overlap)
        
        return RegionDetectedEventDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="RegionDetectedEvent",
                capability_id="CAP-BPR-DETECTION",
                ontology_id="ONT-REGION-DETECTED-EVENT"
            ),
            metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", event_id, {}),
            provenance=EvidenceProvenanceDTO(
                producer_rule="BPRRule",
                execution_mode="Standard",
                execution_timestamp="T", # Would inherit max timestamp of A and B
                source_evidence_ids=[fvg_a.identity.evidence_id, fvg_b.identity.evidence_id],
                market_dataset_id="MKT-1"
            ),
            classification=EvidenceClassification.DERIVED,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            region_identity=region_identity,
            bounds=bounds,
            width=fvg_b.geometry.width, # Rough approximation
            anchor_observation_ids=[]
        )
