import pytest
from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO
from Backend.core.analytical_rules.capabilities.imbalances.fvg_detection_rule import FVGDetectionRule

def _create_observation(obs_id: str, high: float, low: float) -> PriceObservationDTO:
    return PriceObservationDTO(
        observation_id=obs_id,
        timestamp="T",
        high=high,
        low=low,
        open=0.0,
        close=0.0
    )

from Backend.core.analytical_rules.dto.regions.region_identity import RegionType

def test_fvg_detection_positive_bullish_geometry():
    """Test a geometric gap where obs1 high < obs3 low"""
    rule = FVGDetectionRule()
    
    obs1 = _create_observation("obs1", high=100.0, low=90.0)
    obs2 = _create_observation("obs2", high=110.0, low=95.0)
    obs3 = _create_observation("obs3", high=120.0, low=105.0)
    
    event = rule.evaluate([obs1, obs2, obs3])
    
    assert event is not None
    assert event.bounds.lower_bound == 100.0
    assert event.bounds.upper_bound == 105.0
    assert event.region_identity.region_type == RegionType.FVG

def test_fvg_detection_positive_bearish_geometry():
    """Test a geometric gap where obs1 low > obs3 high"""
    rule = FVGDetectionRule()
    
    obs1 = _create_observation("obs1", high=120.0, low=110.0)
    obs2 = _create_observation("obs2", high=115.0, low=100.0)
    obs3 = _create_observation("obs3", high=105.0, low=95.0)
    
    event = rule.evaluate([obs1, obs2, obs3])
    
    assert event is not None
    assert event.bounds.lower_bound == 105.0
    assert event.bounds.upper_bound == 110.0

def test_fvg_detection_negative_no_gap():
    """Test when obs1 and obs3 overlap (no gap)"""
    rule = FVGDetectionRule()
    
    obs1 = _create_observation("obs1", high=100.0, low=90.0)
    obs2 = _create_observation("obs2", high=105.0, low=95.0)
    obs3 = _create_observation("obs3", high=110.0, low=98.0)
    
    # obs1 high is 100.0, obs3 low is 98.0. They overlap.
    event = rule.evaluate([obs1, obs2, obs3])
    assert event is None
