from Backend.core.engine.evidence_quality import EvidenceQualityMetadata
import pytest
from Backend.core.analytical_rules.dto.liquidity.pool_state import PoolState
from Backend.core.analytical_rules.dto.liquidity.pool_identity import PoolIdentityDTO, PoolSide
from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO
from Backend.core.analytical_rules.dto.liquidity.pool_interaction_events import PoolInteractionType
from Backend.core.analytical_rules.capabilities.liquidity.pool_interaction_rule import PoolInteractionRule
from Backend.core.analytical_rules.capabilities.liquidity.pool_lifecycle_engine import PoolLifecycleEngine
from Backend.core.analytical_rules.dto.liquidity.pool_transitions import PoolTransitionType
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

def _create_mock_buyside_pool(lower: float, upper: float) -> PoolState:
    pool_identity = PoolIdentityDTO(
        pool_id="pool_1",
        pool_side=PoolSide.BUY_SIDE,
        anchor_ids=["a1"],
        graph_namespace="liquidity/default",
        policy_checksum="test_policy",
        geometry_fingerprint="test_geom"
    )
    return PoolState(
        identity=EvidenceIdentityDTO(
            evidence_id="pool_1",
            evidence_type="PoolState",
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
            quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),
            superseded_by=None,
            pool_identity=pool_identity,
        lower_bound=lower,
        upper_bound=upper,
        active=True,
        created_at="T0",
        valid_from="T0",
        invalidated_by="null"
    )

def test_interaction_determinism():
    """Verify that replaying identical observations yields identical events"""
    rule = PoolInteractionRule()
    pool = _create_mock_buyside_pool(lower=100.0, upper=102.0)
    
    obs = PriceObservationDTO(
        observation_id="obs_1",
        timestamp="T1",
        high=101.0, # ENTER
        low=90.0,
        open=95.0,
        close=100.0
    )
    
    event1 = rule.evaluate(pool, obs)
    event2 = rule.evaluate(pool, obs)
    
    assert event1 is not None
    assert event2 is not None
    assert event1.interaction_type == event2.interaction_type
    assert event1.maximum_penetration == event2.maximum_penetration
    assert event1.event_id == event2.event_id

def test_boundary_monotonicity():
    """Verify increasing penetrations reflect appropriate types and max penetration amounts"""
    rule = PoolInteractionRule()
    pool = _create_mock_buyside_pool(lower=100.0, upper=102.0)
    
    # Not entered
    obs_none = PriceObservationDTO(observation_id="obs_1", timestamp="T1", high=99.0, low=90.0, open=95.0, close=95.0)
    evt_none = rule.evaluate(pool, obs_none)
    assert evt_none is None
    
    # Enter (past lower, but not upper)
    obs_enter = PriceObservationDTO(observation_id="obs_2", timestamp="T2", high=101.0, low=90.0, open=95.0, close=100.0)
    evt_enter = rule.evaluate(pool, obs_enter)
    assert evt_enter.interaction_type == PoolInteractionType.ENTER
    assert evt_enter.maximum_penetration == 1.0
    
    # Complete Traversal (past upper)
    obs_traversal = PriceObservationDTO(observation_id="obs_3", timestamp="T3", high=103.0, low=90.0, open=95.0, close=102.0)
    evt_traversal = rule.evaluate(pool, obs_traversal)
    assert evt_traversal.interaction_type == PoolInteractionType.COMPLETE_TRAVERSAL
    assert evt_traversal.maximum_penetration == 3.0

def test_lifecycle_integration():
    """Verify PoolLifecycleEngine accurately consumes PoolInteractionEventDTO"""
    engine = PoolLifecycleEngine()
    rule = PoolInteractionRule()
    pool = _create_mock_buyside_pool(lower=100.0, upper=102.0)
    
    # Complete Traversal should invalidate the pool in our foundational wave setup
    obs = PriceObservationDTO(observation_id="obs_1", timestamp="T1", high=105.0, low=90.0, open=95.0, close=95.0)
    event = rule.evaluate(pool, obs)
    
    transition = engine.process_pool_interaction_event(event, pool)
    
    assert transition is not None
    assert transition.transition_type == PoolTransitionType.INVALIDATED
    assert transition.new_state.active is False
    assert transition.new_state.invalidated_by == event.event_id
    assert transition.transition_reason == "Pool invalidated due to COMPLETE_TRAVERSAL interaction"
