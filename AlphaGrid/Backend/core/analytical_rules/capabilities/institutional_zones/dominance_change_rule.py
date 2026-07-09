import uuid
from typing import Optional

from Backend.core.analytical_rules.dto.regions.region_state import RegionState, RegionLifecycleState
from Backend.core.analytical_rules.dto.regions.region_relationships import RegionRelationshipDTO, RegionRelationshipType
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class DominanceChangeRule:
    """
    Detects a flip in dominance between two opposing Regions (e.g. Supply vs Demand).
    This occurs when Region A is invalidated by price action stemming from Region B.
    Emits a RegionRelationshipDTO describing the flip.
    """
    
    def evaluate(self, invalidated_region: RegionState, validating_region: RegionState) -> Optional[RegionRelationshipDTO]:
        if invalidated_region.lifecycle_state != RegionLifecycleState.INVALIDATED:
            return None
            
        event_id = f"DOMINANCE-CHANGE-{uuid.uuid4()}"
        
        return RegionRelationshipDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="RegionRelationship",
                capability_id="CAP-DOMINANCE-DETECTION",
                ontology_id="ONT-REGION-RELATIONSHIP"
            ),
            metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", event_id, {}),
            provenance=EvidenceProvenanceDTO(
                producer_rule="DominanceChangeRule",
                execution_mode="Standard",
                execution_timestamp="T",
                source_evidence_ids=[invalidated_region.identity.evidence_id, validating_region.identity.evidence_id],
                market_dataset_id="MKT-1"
            ),
            classification=EvidenceClassification.DERIVED,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            source_region_id=validating_region.region_identity.region_id,
            target_region_id=invalidated_region.region_identity.region_id,
            relationship_type=RegionRelationshipType.DOMINANCE_CHANGE,
            relationship_metadata={
                "source_type": validating_region.region_identity.region_type.value,
                "target_type": invalidated_region.region_identity.region_type.value
            }
        )
