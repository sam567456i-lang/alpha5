import pytest
from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO
from Backend.core.analytical_rules.dto.regions.region_identity import RegionIdentityDTO, RegionType
from Backend.core.analytical_rules.dto.regions.region_geometry import RegionBoundsDTO, RegionGeometryDTO
from Backend.core.analytical_rules.dto.regions.region_context import RegionInteractionContextDTO
from Backend.core.analytical_rules.dto.regions.region_events import RegionReferenceType
from Backend.core.analytical_rules.capabilities.regions.region_interaction_rule import RegionInteractionRule

def _create_region() -> (RegionIdentityDTO, RegionGeometryDTO):
    identity = RegionIdentityDTO("reg_1", RegionType.FVG, ["o1", "o2", "o3"], "namespace", "policy", "fp")
    bounds = RegionBoundsDTO(upper_bound=100.0, lower_bound=50.0)
    geom = RegionGeometryDTO(bounds=bounds, width=3.0, area=150.0, geometry_fingerprint="fp")
    return identity, geom

def test_region_interaction_center():
    rule = RegionInteractionRule()
    identity, geom = _create_region()
    
    # Observation that crosses the center (75.0)
    obs = PriceObservationDTO("obs1", "T", high=80.0, low=70.0, open=75.0, close=75.0)
    
    context = RegionInteractionContextDTO(
        region_identity=identity,
        region_geometry=geom,
        observation=obs,
        target_references=[RegionReferenceType.CENTER],
        policy_overrides={}
    )
    
    events = rule.evaluate(context)
    
    assert len(events) == 1
    assert events[0].reference_type == RegionReferenceType.CENTER
    assert events[0].interaction_price == 75.0

def test_region_interaction_full_fill():
    rule = RegionInteractionRule()
    identity, geom = _create_region()
    
    # Observation that completely covers the region bounds [50.0, 100.0]
    obs = PriceObservationDTO("obs1", "T", high=110.0, low=40.0, open=60.0, close=90.0)
    
    context = RegionInteractionContextDTO(
        region_identity=identity,
        region_geometry=geom,
        observation=obs,
        target_references=[RegionReferenceType.FILL_FULL],
        policy_overrides={}
    )
    
    events = rule.evaluate(context)
    
    assert len(events) == 1
    assert events[0].reference_type == RegionReferenceType.FILL_FULL

def test_region_interaction_no_fill():
    rule = RegionInteractionRule()
    identity, geom = _create_region()
    
    # Observation above the region
    obs = PriceObservationDTO("obs1", "T", high=120.0, low=110.0, open=115.0, close=115.0)
    
    context = RegionInteractionContextDTO(
        region_identity=identity,
        region_geometry=geom,
        observation=obs,
        target_references=[RegionReferenceType.FILL_FULL, RegionReferenceType.CENTER],
        policy_overrides={}
    )
    
    events = rule.evaluate(context)
    
    assert len(events) == 0
