import pytest
from Backend.core.analytical_rules.dto.liquidity.pool_events import PoolDetectedEventDTO
from Backend.core.analytical_rules.dto.liquidity.pool_identity import PoolIdentityDTO, PoolSide
from Backend.core.analytical_rules.dto.liquidity.pool_transitions import PoolTransitionType
from Backend.core.analytical_rules.capabilities.liquidity.pool_lifecycle_engine import PoolLifecycleEngine
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

def test_pool_lifecycle_creation():
    engine = PoolLifecycleEngine()
    
    pool_identity = PoolIdentityDTO(
        pool_id="pool_1",
        pool_side=PoolSide.BUY_SIDE,
        anchor_ids=["a1", "a2"],
        graph_namespace="liquidity/default",
        policy_checksum="test_policy",
        geometry_fingerprint="test_geom"
    )
    
    event = PoolDetectedEventDTO(
        identity=EvidenceIdentityDTO(
            evidence_id="event_1",
            evidence_type="PoolDetectedEvent",
            capability_id="TEST",
            ontology_id="TEST"
        ),
        metadata=EvidenceMetadataDTO(
            schema_version="1.0",
            rule_version="1.0",
            rule_checksum="none",
            registry_checksum="none",
            sdk_version="1.0",
            planner_version="1.0",
            fingerprint="event_fingerprint",
            custom_tags={}
        ),
        provenance=EvidenceProvenanceDTO(
            producer_rule="Test",
            execution_mode="Test",
            execution_timestamp="T0",
            source_evidence_ids=[],
            market_dataset_id="TEST"
        ),
        classification=EvidenceClassification.COMPOSITE,
        interpretation_level=InterpretationLevel.OBJECTIVE,
        validity_status=ValidityStatus.ACTIVE,
        evidence_data={},
        event_id="event_1",
        event_timestamp="T0",
        trigger_rule="test",
        trigger_evidence="test",
        affected_state_ids=[],
        causal_events=[],
        severity="INFO",
        sequence_number=1,
        confidence_inputs=["ci_1"],
        pool_identity=pool_identity,
        center_price=100.0,
        upper_bound=101.0,
        lower_bound=99.0,
        width=2.0,
        anchor_distribution="UNIFORM",
        supporting_evidence_ids=["a1", "a2"],
        supporting_state_ids=["state_1"],
        policy_version="1.0",
        detection_reason="test"
    )
    
    transition = engine.process_pool_detected_event(event)
    
    assert transition.pool_id == "pool_1"
    assert transition.transition_type == PoolTransitionType.CREATED
    assert transition.previous_state is None
    assert transition.trigger_event_id == "event_1"
    
    new_state = transition.new_state
    
    # Assert geometry is mapped over
    assert new_state.center_price == 100.0
    assert new_state.upper_bound == 101.0
    assert new_state.lower_bound == 99.0
    assert new_state.width == 2.0
    
    # Assert lifecycle metadata is correct
    assert new_state.created_by_event == "event_1"
    assert new_state.created_at == "T0"
    assert new_state.active is True
    
    # Assert provenance
    assert new_state.supporting_evidence_ids == ["a1", "a2"]
    assert new_state.confidence_inputs == ["ci_1"]
    
    # Assert relationships are empty
    assert new_state.parent_pool_id is None
    assert len(new_state.derived_pool_ids) == 0
    assert new_state.superseded_by is None
    assert new_state.invalidated_by is None
    assert new_state.consumed_by is None
