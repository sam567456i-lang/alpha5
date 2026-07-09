import pytest
from Backend.core.analytical_rules.dto.liquidity.equal_primitives import EqualHighState, EqualLowState
from Backend.core.analytical_rules.capabilities.liquidity.pool_detector import BuySidePoolDetector, SellSidePoolDetector, PoolDetectionPolicy
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

def _create_mock_equal_high_state(state_id: str, count: int, price: float, price_variance: float = 0.0) -> EqualHighState:
    return EqualHighState(
        identity=EvidenceIdentityDTO(
            evidence_id=state_id,
            evidence_type="EqualHighState",
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
            fingerprint="test",
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
        state_id=state_id,
        created_at="T0",
        valid_from="T0",
        valid_until="null",
        is_active=True,
        invalidated_at="null",
        invalidated_by="null",
        superseded_by="null",
        related_state_ids=[],
        related_event_ids=[],
        confidence_inputs=[],
        anchor_ids=["a" + str(i) for i in range(count)],
        anchor_count=count,
        average_price=price,
        price_variance=price_variance
    )

def _create_mock_equal_low_state(state_id: str, count: int, price: float, price_variance: float = 0.0) -> EqualLowState:
    return EqualLowState(
        identity=EvidenceIdentityDTO(
            evidence_id=state_id,
            evidence_type="EqualLowState",
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
            fingerprint="test",
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
        state_id=state_id,
        created_at="T0",
        valid_from="T0",
        valid_until="null",
        is_active=True,
        invalidated_at="null",
        invalidated_by="null",
        superseded_by="null",
        related_state_ids=[],
        related_event_ids=[],
        confidence_inputs=[],
        anchor_ids=["a" + str(i) for i in range(count)],
        anchor_count=count,
        average_price=price,
        price_variance=price_variance
    )

def test_buyside_pool_detection():
    policy = PoolDetectionPolicy(minimum_anchor_count=3, price_buffer=0.5)
    detector = BuySidePoolDetector(policy)
    
    eqh_states = [
        _create_mock_equal_high_state("eqh_1", count=2, price=100.0), # Too few anchors
        _create_mock_equal_high_state("eqh_2", count=3, price=110.0, price_variance=2.0), # Valid
        _create_mock_equal_high_state("eqh_3", count=4, price=120.0)  # Valid
    ]
    
    events = detector.detect(eqh_states)
    
    assert len(events) == 2
    
    # Event 0 mapping to eqh_2
    assert events[0].supporting_state_ids == ["eqh_2"]
    assert events[0].pool_identity.pool_side.value == "BUY_SIDE"
    assert events[0].center_price == 110.0
    # upper_bound = center_price + (variance/2) + price_buffer = 110.0 + 1.0 + 0.5 = 111.5
    assert events[0].upper_bound == 111.5
    # lower_bound = center_price - (variance/2) = 110.0 - 1.0 = 109.0
    assert events[0].lower_bound == 109.0
    assert events[0].width == 2.5
    
    # Event 1 mapping to eqh_3
    assert events[1].supporting_state_ids == ["eqh_3"]
    assert events[1].pool_identity.pool_side.value == "BUY_SIDE"
    assert events[1].center_price == 120.0


def test_sellside_pool_detection():
    policy = PoolDetectionPolicy(minimum_anchor_count=2, price_buffer=0.5)
    detector = SellSidePoolDetector(policy)
    
    eql_states = [
        _create_mock_equal_low_state("eql_1", count=1, price=50.0), # Too few anchors
        _create_mock_equal_low_state("eql_2", count=2, price=40.0, price_variance=1.0), # Valid
    ]
    
    events = detector.detect(eql_states)
    
    assert len(events) == 1
    
    assert events[0].supporting_state_ids == ["eql_2"]
    assert events[0].pool_identity.pool_side.value == "SELL_SIDE"
    assert events[0].center_price == 40.0
    # upper_bound = center_price + (variance/2) = 40.0 + 0.5 = 40.5
    assert events[0].upper_bound == 40.5
    # lower_bound = center_price - (variance/2) - price_buffer = 40.0 - 0.5 - 0.5 = 39.0
    assert events[0].lower_bound == 39.0
    assert events[0].width == 1.5
