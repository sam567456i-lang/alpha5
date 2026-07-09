import uuid
from typing import Optional

from Backend.core.analytical_rules.dto.regions.region_state import RegionState
from Backend.core.analytical_rules.dto.regions.region_relationships import RegionRelationshipDTO, RegionRelationshipType
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class SequentialInteractionRule:
    """
    Detects when Region B is created out of a successful interaction with Region A.
    This objective sequence is typically interpreted by ICT methodologies as a Propulsion Block
    (when an Order Block mitigates another Order Block).
    Emits a RegionRelationshipDTO describing the derivation.
    """
    
    def evaluate(self, source_region: RegionState, derived_region: RegionState) -> RegionRelationshipDTO:
        event_id = f"SEQ-INTERACTION-{uuid.uuid4()}"
        
        return RegionRelationshipDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="RegionRelationship",
                capability_id="CAP-SEQUENTIAL-INTERACTION-DETECTION",
                ontology_id="ONT-REGION-RELATIONSHIP"
            ),
            metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", event_id, {}),
            provenance=EvidenceProvenanceDTO(
                producer_rule="SequentialInteractionRule",
                execution_mode="Standard",
                execution_timestamp="T",
                source_evidence_ids=[source_region.identity.evidence_id, derived_region.identity.evidence_id],
                market_dataset_id="MKT-1"
            ),
            classification=EvidenceClassification.DERIVED,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            source_region_id=source_region.region_identity.region_id,
            target_region_id=derived_region.region_identity.region_id,
            relationship_type=RegionRelationshipType.DERIVED_FROM,
            relationship_metadata={
                "source_type": source_region.region_identity.region_type.value,
                "derived_type": derived_region.region_identity.region_type.value,
                "description": "Region B was created during interaction with Region A"
            }
        )
