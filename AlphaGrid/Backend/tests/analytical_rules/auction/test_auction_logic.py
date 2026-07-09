import pytest
from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO
from Backend.core.analytical_rules.dto.regions.region_state import RegionState, RegionLifecycleState
from Backend.core.analytical_rules.dto.regions.region_identity import RegionIdentityDTO, RegionType
from Backend.core.analytical_rules.dto.regions.region_geometry import RegionBoundsDTO, RegionGeometryDTO
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

from Backend.core.analytical_rules.capabilities.auction.auction_rule import AuctionMetricsRule

def _mock_region_state() -> RegionState:
    identity = RegionIdentityDTO("reg_1", RegionType.FVG, ["a", "b"], "regions/test", "none", "fp")
    bounds = RegionBoundsDTO(upper_bound=110.0, lower_bound=100.0)
    geom = RegionGeometryDTO(bounds=bounds, width=3.0, area=30.0, geometry_fingerprint="fp")
    
    return RegionState(
        identity=EvidenceIdentityDTO("state_1", "RegionState", "CAP", "ONT"),
        metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", "fp", {}),
        provenance=EvidenceProvenanceDTO("Engine", "Standard", "T", [], "MKT-1"),
        classification=EvidenceClassification.COMPOSITE,
        interpretation_level=InterpretationLevel.OBJECTIVE,
        validity_status=ValidityStatus.ACTIVE,
        evidence_data={},
        region_identity=identity,
        geometry=geom,
        lifecycle_state=RegionLifecycleState.CREATED,
        remaining_height=10.0
    )

def test_auction_metrics_rule():
    rule = AuctionMetricsRule()
    region = _mock_region_state()
    
    # 1. outside below
    # 2. inside (entry)
    # 3. inside
    # 4. outside above (exit)
    # 5. inside (entry)
    obs = [
        PriceObservationDTO("obs_1", "T1", high=95.0, low=90.0, open=92.0, close=94.0),
        PriceObservationDTO("obs_2", "T2", high=105.0, low=95.0, open=96.0, close=104.0), # Entry
        PriceObservationDTO("obs_3", "T3", high=108.0, low=102.0, open=104.0, close=106.0), # Inside
        PriceObservationDTO("obs_4", "T4", high=115.0, low=111.0, open=112.0, close=114.0), # Exit
        PriceObservationDTO("obs_5", "T5", high=105.0, low=95.0, open=112.0, close=100.0)   # Entry
    ]
    
    metrics = rule.evaluate(region, obs)
    
    assert metrics is not None
    assert metrics.number_of_entries == 2
    assert metrics.number_of_exits == 1
    assert metrics.time_inside_region == 3
    assert metrics.volume_inside_region == 300.0
