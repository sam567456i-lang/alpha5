from Backend.core.engine.evidence_quality import EvidenceQualityMetadata
from typing import List, Dict, Any, Union
from Backend.core.analytical_rules.dto.liquidity.equal_primitives_events import EqualHighDetectedEventDTO, EqualLowDetectedEventDTO
from Backend.core.analytical_rules.dto.liquidity.equal_primitives import EqualHighState, EqualLowState
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus
from Backend.core.analytical_rules.utils.identity_factory import IdentityFactory

class EqualPrimitiveLifecycleEngine:
    """
    Consumes EqualHighDetectedEventDTO or EqualLowDetectedEventDTO and projects them 
    into persistent EqualHighState or EqualLowState nodes.
    Also manages Supersession and Invalidation (to be expanded in later waves).
    """
    
    def process_high_event(self, event: EqualHighDetectedEventDTO) -> EqualHighState:
        # Create state from event
        state_id = IdentityFactory.generate_state_id("EQH", event.event_id)
        
        return EqualHighState(
            identity=EvidenceIdentityDTO(
                evidence_id=state_id,
                evidence_type="EqualHighState",
                capability_id="CAP-LIQUIDITY-01",
                ontology_id="ONT-LIQUIDITY-EQH"
            ),
            metadata=EvidenceMetadataDTO(
                schema_version="1.0.0",
                rule_version="1.0.0",
                rule_checksum="none",
                registry_checksum="none",
                sdk_version="1.0.0",
                planner_version="1.0.0",
                fingerprint=event.metadata.fingerprint,
                custom_tags={}
            ),
            provenance=EvidenceProvenanceDTO(
                producer_rule="EqualPrimitiveLifecycleEngine",
                execution_mode="Standard",
                execution_timestamp=event.event_timestamp,
                source_evidence_ids=[event.event_id],
                market_dataset_id="MKT-123"
            ),
            classification=EvidenceClassification.COMPOSITE,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),
            state_id=state_id,
            created_at=event.event_timestamp,
            valid_from=event.event_timestamp,
            valid_until="null",
            is_active=True,
            invalidated_at="null",
            invalidated_by="null",
            superseded_by="null",
            related_state_ids=[],
            related_event_ids=[event.event_id],
            confidence_inputs=[],
            anchor_ids=event.anchor_ids,
            anchor_count=event.anchor_count,
            average_price=event.average_price,
            price_variance=event.price_variance
        )

    def process_low_event(self, event: EqualLowDetectedEventDTO) -> EqualLowState:
        # Create state from event
        state_id = IdentityFactory.generate_state_id("EQL", event.event_id)
        
        return EqualLowState(
            identity=EvidenceIdentityDTO(
                evidence_id=state_id,
                evidence_type="EqualLowState",
                capability_id="CAP-LIQUIDITY-02",
                ontology_id="ONT-LIQUIDITY-EQL"
            ),
            metadata=EvidenceMetadataDTO(
                schema_version="1.0.0",
                rule_version="1.0.0",
                rule_checksum="none",
                registry_checksum="none",
                sdk_version="1.0.0",
                planner_version="1.0.0",
                fingerprint=event.metadata.fingerprint,
                custom_tags={}
            ),
            provenance=EvidenceProvenanceDTO(
                producer_rule="EqualPrimitiveLifecycleEngine",
                execution_mode="Standard",
                execution_timestamp=event.event_timestamp,
                source_evidence_ids=[event.event_id],
                market_dataset_id="MKT-123"
            ),
            classification=EvidenceClassification.COMPOSITE,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),
            state_id=state_id,
            created_at=event.event_timestamp,
            valid_from=event.event_timestamp,
            valid_until="null",
            is_active=True,
            invalidated_at="null",
            invalidated_by="null",
            superseded_by="null",
            related_state_ids=[],
            related_event_ids=[event.event_id],
            confidence_inputs=[],
            anchor_ids=event.anchor_ids,
            anchor_count=event.anchor_count,
            average_price=event.average_price,
            price_variance=event.price_variance
        )
