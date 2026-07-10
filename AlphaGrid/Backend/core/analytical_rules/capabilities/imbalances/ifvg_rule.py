from Backend.core.engine.evidence_quality import EvidenceQualityMetadata
import uuid
from typing import Optional

from Backend.core.analytical_rules.dto.regions.region_events import RegionDetectedEventDTO
from Backend.core.analytical_rules.dto.regions.region_identity import RegionIdentityDTO, RegionType
from Backend.core.analytical_rules.dto.regions.region_state import RegionState, RegionLifecycleState
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class IFVGRule:
    """
    Derived rule that creates an Inversion Fair Value Gap (IFVG) region 
    when an existing FVG region reaches FULLY_FILLED lifecycle state.
    Strictly consumes certified state evidence. No raw candle inspection.
    """
    
    def evaluate(self, state: RegionState) -> Optional[RegionDetectedEventDTO]:
        if state.region_identity.region_type != RegionType.FVG:
            return None
            
        if state.lifecycle_state != RegionLifecycleState.FULLY_FILLED:
            return None
            
        event_id = f"IFVG-DETECTED-{uuid.uuid4()}"
        region_id = f"REGION-IFVG-{uuid.uuid4()}"
        
        region_identity = RegionIdentityDTO(
            region_id=region_id,
            region_type=RegionType.IFVG,
            anchor_ids=[state.identity.evidence_id], # Anchored to the original FVG state
            graph_namespace="regions/ifvg",
            policy_checksum="none",
            geometry_fingerprint=state.geometry.geometry_fingerprint
        )
        
        return RegionDetectedEventDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="RegionDetectedEvent",
                capability_id="CAP-IFVG-DETECTION",
                ontology_id="ONT-REGION-DETECTED-EVENT"
            ),
            metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", event_id, {}),
            provenance=EvidenceProvenanceDTO(
                producer_rule="IFVGRule",
                execution_mode="Standard",
                execution_timestamp="T", # Would inherit from the interaction event that caused FULL_FILL
                source_evidence_ids=[state.identity.evidence_id],
                market_dataset_id="MKT-1"
            ),
            classification=EvidenceClassification.DERIVED,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),
            superseded_by=None,
            region_identity=region_identity,
            bounds=state.geometry.bounds,
            width=state.geometry.width,
            anchor_observation_ids=[]
        )
