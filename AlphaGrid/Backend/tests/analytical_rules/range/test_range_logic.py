import pytest
from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO
from Backend.core.analytical_rules.dto.liquidity.pool_state import PoolState
from Backend.core.analytical_rules.dto.liquidity.pool_identity import PoolIdentityDTO, PoolSide
from Backend.core.analytical_rules.dto.range.range_state import RangeState, RangePolicy
from Backend.core.analytical_rules.capabilities.range.premium_discount_rule import PremiumDiscountRule, RangeZone
from Backend.core.analytical_rules.capabilities.range.liquidity_relationship_rule import RangeLiquidityRelationshipRule, RangeLiquidityLocation
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

def test_premium_discount_rule():
    policy = RangePolicy(equilibrium_reference=0.5, premium_boundary=0.5, discount_boundary=0.5)
    
    range_state = RangeState(
        identity=EvidenceIdentityDTO("range_evt", "RangeState", "CAP", "ONT"),
        metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", "fp", {}),
        provenance=EvidenceProvenanceDTO("Engine", "Standard", "T", [], "MKT-1"),
        classification=EvidenceClassification.COMPOSITE,
        interpretation_level=InterpretationLevel.OBJECTIVE,
        validity_status=ValidityStatus.ACTIVE,
        evidence_data={},
        range_id="range_1",
        upper_bound=100.0,
        lower_bound=0.0,
        policy=policy
    )
    
    rule = PremiumDiscountRule()
    
    obs_premium = PriceObservationDTO("obs_1", "T", high=85.0, low=75.0, open=80.0, close=80.0) # typical = 80
    obs_discount = PriceObservationDTO("obs_2", "T", high=30.0, low=20.0, open=25.0, close=25.0) # typical = 25
    obs_eq = PriceObservationDTO("obs_3", "T", high=55.0, low=45.0, open=50.0, close=50.0) # typical = 50
    
    assert rule.evaluate(range_state, obs_premium) == RangeZone.PREMIUM
    assert rule.evaluate(range_state, obs_discount) == RangeZone.DISCOUNT
    assert rule.evaluate(range_state, obs_eq) == RangeZone.EQUILIBRIUM # if >= premium or <= discount handles equality? Actually 50 is >= 50, so it might be PREMIUM.

def test_liquidity_relationship_rule():
    policy = RangePolicy()
    range_state = RangeState(
        identity=EvidenceIdentityDTO("range_evt", "RangeState", "CAP", "ONT"),
        metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", "fp", {}),
        provenance=EvidenceProvenanceDTO("Engine", "Standard", "T", [], "MKT-1"),
        classification=EvidenceClassification.COMPOSITE,
        interpretation_level=InterpretationLevel.OBJECTIVE,
        validity_status=ValidityStatus.ACTIVE,
        evidence_data={},
        range_id="range_1",
        upper_bound=100.0,
        lower_bound=0.0,
        policy=policy
    )
    
    def mock_pool(price):
        ident = PoolIdentityDTO("pool_1", PoolSide.BUY_SIDE, [], "regions/pool", "none", "fp")
        return PoolState(
            identity=EvidenceIdentityDTO("state_1", "LiquidityPoolState", "CAP", "ONT"),
            metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", "fp", {}),
            provenance=EvidenceProvenanceDTO("Engine", "Standard", "T", [], "MKT-1"),
            classification=EvidenceClassification.COMPOSITE,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            pool_identity=ident,
            center_price=price,
            upper_bound=price + 0.5,
            lower_bound=price - 0.5,
            width=1.0,
            anchor_distribution="UNIFORM",
            created_by_event="T1",
            created_at="T1",
            valid_from="T1",
            last_updated="T2",
            active=True
        )

    rule = RangeLiquidityRelationshipRule()
    
    rel_boundary = rule.evaluate(range_state, mock_pool(100.0))
    assert rel_boundary.location == RangeLiquidityLocation.BOUNDARY
    
    rel_inside = rule.evaluate(range_state, mock_pool(50.0))
    assert rel_inside.location == RangeLiquidityLocation.INSIDE
    
    rel_outside = rule.evaluate(range_state, mock_pool(150.0))
    assert rel_outside.location == RangeLiquidityLocation.OUTSIDE
