from Backend.core.engine.evidence_quality import EvidenceQualityMetadata
import pytest
from Backend.core.analytical_rules.dto.regions.region_identity import RegionIdentityDTO, RegionType
from Backend.core.analytical_rules.dto.regions.region_geometry import RegionBoundsDTO, RegionGeometryDTO
from Backend.core.analytical_rules.dto.regions.region_state import RegionState, RegionLifecycleState
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

from Backend.core.analytical_rules.capabilities.imbalances.ifvg_rule import IFVGRule
from Backend.core.analytical_rules.capabilities.imbalances.bpr_rule import BPRRule
from Backend.core.analytical_rules.capabilities.imbalances.liquidity_void_rule import LiquidityVoidRule

def _mock_fvg_state(region_id: str, upper: float, lower: float, state: RegionLifecycleState = RegionLifecycleState.CREATED) -> RegionState:
    identity = RegionIdentityDTO(region_id, RegionType.FVG, ["a", "b"], "regions/fvg", "none", f"{lower}-{upper}")
    bounds = RegionBoundsDTO(upper_bound=upper, lower_bound=lower)
    geom = RegionGeometryDTO(bounds=bounds, width=3.0, area=(upper-lower)*3, geometry_fingerprint="fp")
    
    return RegionState(
        identity=EvidenceIdentityDTO(f"state_{region_id}", "ImbalanceState", "CAP", "ONT"),
        metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", "fp", {}),
        provenance=EvidenceProvenanceDTO("Engine", "Standard", "T", [], "MKT-1"),
        classification=EvidenceClassification.COMPOSITE,
        interpretation_level=InterpretationLevel.OBJECTIVE,
        validity_status=ValidityStatus.ACTIVE,
        evidence_data={},
        region_identity=identity,
        geometry=geom,
        lifecycle_state=state,
        remaining_height=upper-lower
    )

def test_ifvg_rule():
    rule = IFVGRule()
    # Not fully filled FVG
    active_fvg = _mock_fvg_state("fvg_1", upper=110.0, lower=100.0, state=RegionLifecycleState.CREATED)
    assert rule.evaluate(active_fvg) is None
    
    # Fully filled FVG -> Should become IFVG
    filled_fvg = _mock_fvg_state("fvg_2", upper=110.0, lower=100.0, state=RegionLifecycleState.FULLY_FILLED)
    event = rule.evaluate(filled_fvg)
    
    assert event is not None
    assert event.region_identity.region_type == RegionType.IFVG
    assert event.bounds.upper_bound == 110.0
    assert event.bounds.lower_bound == 100.0

def test_bpr_rule():
    rule = BPRRule()
    fvg_a = _mock_fvg_state("fvg_a", upper=110.0, lower=100.0)
    
    # Overlapping FVG B
    fvg_b_overlap = _mock_fvg_state("fvg_b", upper=105.0, lower=95.0)
    event_overlap = rule.evaluate(fvg_a, fvg_b_overlap)
    
    assert event_overlap is not None
    assert event_overlap.region_identity.region_type == RegionType.BPR
    assert event_overlap.bounds.upper_bound == 105.0
    assert event_overlap.bounds.lower_bound == 100.0
    
    # Non-overlapping FVG C
    fvg_c_no_overlap = _mock_fvg_state("fvg_c", upper=95.0, lower=85.0)
    assert rule.evaluate(fvg_a, fvg_c_no_overlap) is None

def test_liquidity_void_rule():
    rule = LiquidityVoidRule()
    fvg_1 = _mock_fvg_state("fvg_1", upper=130.0, lower=120.0)
    fvg_2 = _mock_fvg_state("fvg_2", upper=120.0, lower=110.0)
    fvg_3 = _mock_fvg_state("fvg_3", upper=110.0, lower=100.0)
    
    event = rule.evaluate([fvg_1, fvg_2, fvg_3])
    
    assert event is not None
    assert event.region_identity.region_type == RegionType.LIQUIDITY_VOID
    assert event.bounds.upper_bound == 130.0
    assert event.bounds.lower_bound == 100.0
