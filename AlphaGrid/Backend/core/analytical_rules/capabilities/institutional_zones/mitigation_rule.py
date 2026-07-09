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

class MitigationRule:
    """
    Derived rule that emits a MITIGATION_BLOCK Region when an Order Block RegionState is INVALIDATED,
    provided there is an associated structural event indicating price continued past it
    without first establishing a structural extreme beyond it.
    Strictly consumes objective state evidence.
    """
    
    def evaluate(self, state: RegionState, structure_event: EvidenceIdentityDTO) -> Optional[RegionDetectedEventDTO]:
        if state.region_identity.region_type != RegionType.ORDER_BLOCK:
            return None
            
        if state.lifecycle_state != RegionLifecycleState.INVALIDATED:
            return None
            
        event_id = f"MITIGATION-DETECTED-{uuid.uuid4()}"
        region_id = f"REGION-MITIGATION-{uuid.uuid4()}"
        
        region_identity = RegionIdentityDTO(
            region_id=region_id,
            region_type=RegionType.MITIGATION_BLOCK,
            anchor_ids=[state.identity.evidence_id, structure_event.evidence_id],
            graph_namespace="regions/mitigation",
            policy_checksum="none",
            geometry_fingerprint=state.geometry.geometry_fingerprint
        )
        
        return RegionDetectedEventDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="RegionDetectedEvent",
                capability_id="CAP-MITIGATION-DETECTION",
                ontology_id="ONT-REGION-DETECTED-EVENT"
            ),
            metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", event_id, {}),
            provenance=EvidenceProvenanceDTO(
                producer_rule="MitigationRule",
                execution_mode="Standard",
                execution_timestamp="T",
                source_evidence_ids=[state.identity.evidence_id, structure_event.evidence_id],
                market_dataset_id="MKT-1"
            ),
            classification=EvidenceClassification.DERIVED,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            region_identity=region_identity,
            bounds=state.geometry.bounds,
            width=state.geometry.width,
            anchor_observation_ids=[]
        )
