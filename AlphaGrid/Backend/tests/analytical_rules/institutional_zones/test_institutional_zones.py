import pytest
from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO
from Backend.core.analytical_rules.dto.regions.region_identity import RegionType
from Backend.core.analytical_rules.dto.regions.region_geometry import OrderBlockGeometryDTO
from Backend.core.analytical_rules.capabilities.institutional_zones.order_block_rule import OrderBlockDetectionRule
from Backend.core.analytical_rules.capabilities.institutional_zones.rejection_block_rule import RejectionBlockDetectionRule

def test_order_block_detection():
    rule = OrderBlockDetectionRule()
    
    # Mock candle: High 110, Low 90, Open 95, Close 105
    obs = PriceObservationDTO("obs_1", "T", high=110.0, low=90.0, open=95.0, close=105.0)
    event = rule.evaluate(obs, "struct_1")
    
    assert event is not None
    assert event.region_identity.region_type == RegionType.ORDER_BLOCK
    
    geom = event.region_identity.geometry_fingerprint
    assert geom is not None
    
    # To test actual geometry dto fields, we inspect the returned bounds
    assert event.bounds.upper_bound == 110.0
    assert event.bounds.lower_bound == 90.0

def test_rejection_block_detection_high():
    rule = RejectionBlockDetectionRule()
    
    # Mock swing high candle: High 110, Low 90, Open 95, Close 100
    # Wick is from 100 to 110
    obs = PriceObservationDTO("obs_1", "T", high=110.0, low=90.0, open=95.0, close=100.0)
    event = rule.evaluate(obs, "struct_1", is_swing_high=True)
    
    assert event is not None
    assert event.region_identity.region_type == RegionType.REJECTION_BLOCK
    assert event.bounds.upper_bound == 110.0
    assert event.bounds.lower_bound == 100.0

def test_rejection_block_detection_low():
    rule = RejectionBlockDetectionRule()
    
    # Mock swing low candle: High 110, Low 90, Open 105, Close 100
    # Wick is from 90 to 100
    obs = PriceObservationDTO("obs_1", "T", high=110.0, low=90.0, open=105.0, close=100.0)
    event = rule.evaluate(obs, "struct_1", is_swing_high=False)
    
    assert event is not None
    assert event.region_identity.region_type == RegionType.REJECTION_BLOCK
    assert event.bounds.upper_bound == 100.0
    assert event.bounds.lower_bound == 90.0
