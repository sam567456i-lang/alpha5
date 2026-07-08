import pytest
from datetime import datetime, timezone
import yaml
import os

from Backend.shared_domain.contracts.zones.zone_dtos import ZoneDTO, ZoneGeometryDTO, ZoneIdentityDTO, ZoneMetadataDTO, ZoneLifecycleStatus
from Backend.platforms.platform9_concepts.zone_features import ZoneFeature
from Backend.platforms.platform9_concepts.feature_base import FeatureType
from Backend.platforms.platform9_concepts.plugins.gap_concepts import FVGConceptPlugin
from Backend.platforms.platform9_concepts.plugins.block_concepts import OrderBlockConceptPlugin, BreakerConceptPlugin
from Backend.core.state import ExecutionContext

def create_mock_zone(z_id: str, z_type: str, status: ZoneLifecycleStatus) -> ZoneDTO:
    identity = ZoneIdentityDTO(
        zone_id=z_id, zone_version=1, previous_version_id=None, root_zone_id=z_id,
        zone_type=z_type, ontology_id="ONT-001", capability_id="CAP-001",
        market="NASDAQ", asset_class="Equities", exchange="NASDAQ", symbol="AAPL",
        timeframe="H1", session_id="RTH", source_detector="MockDetector", registry_version="1.0.0"
    )
    geometry = ZoneGeometryDTO(upper_price=100.0, lower_price=90.0)
    metadata = ZoneMetadataDTO(
        registry_version="1.0.0", fingerprint_hash="hash123", created_by="test",
        detector="MockDetector", latency_ms=1.0, confidence_model="N/A", freshness_model="N/A"
    )
    return ZoneDTO(
        identity=identity, geometry=geometry, metadata=metadata,
        status=status, created_at=datetime.now(timezone.utc)
    )

@pytest.fixture
def context():
    return ExecutionContext(
        session_id="S1", trace_id="T1", correlation_id="C1", instrument_id="AAPL",
        environment="TEST", runtime_mode="TEST", exchange="NASDAQ", provider="MOCK",
        market="NASDAQ", timezone="UTC", sequence_id=1, is_replay=False, build_version="1.0"
    )

def test_geometry_immutability(context):
    zone = create_mock_zone("z1", "GAP_ZONE", ZoneLifecycleStatus.ACTIVE)
    feature_type = FeatureType(id="ZONE_FEATURE", name="Zone Feature", family="SPATIAL")
    feature = ZoneFeature(
        context=context, feature_id="", feature_type=feature_type, version=1, 
        quality=1.0, confidence=1.0, produced_at=datetime.now(timezone.utc),
        zone_dto=zone
    )
    plugin = FVGConceptPlugin()
    
    concepts = plugin.extract([feature], context)
    assert len(concepts) == 1
    
    concept = concepts[0]
    concept.freeze()
    
    # 1. Byte-for-byte immutability test
    # The ZoneDTO inside the feature inside the concept should be exactly the same object.
    extracted_zone = concept.source_features[0].zone_dto
    assert extracted_zone is zone
    assert extracted_zone.geometry.upper_price == 100.0

def test_invalid_mapping(context):
    # Pass a BLOCK_ZONE to the FVG plugin
    zone = create_mock_zone("z1", "BLOCK_ZONE", ZoneLifecycleStatus.ACTIVE)
    feature_type = FeatureType(id="ZONE_FEATURE", name="Zone Feature", family="SPATIAL")
    feature = ZoneFeature(
        context=context, feature_id="", feature_type=feature_type, version=1, 
        quality=1.0, confidence=1.0, produced_at=datetime.now(timezone.utc),
        zone_dto=zone
    )
    plugin = FVGConceptPlugin()
    concepts = plugin.extract([feature], context)
    # Must fail to map
    assert len(concepts) == 0

def test_multiple_concepts_from_one_zone(context):
    # A single BLOCK_ZONE can be evaluated by OB plugin and Breaker Plugin.
    # We set status to INVALIDATED to trigger Breaker logic as well.
    zone = create_mock_zone("z1", "BLOCK_ZONE", ZoneLifecycleStatus.INVALIDATED)
    feature_type = FeatureType(id="ZONE_FEATURE", name="Zone Feature", family="SPATIAL")
    feature = ZoneFeature(
        context=context, feature_id="", feature_type=feature_type, version=1, 
        quality=1.0, confidence=1.0, produced_at=datetime.now(timezone.utc),
        zone_dto=zone
    )
    ob_plugin = OrderBlockConceptPlugin()
    brk_plugin = BreakerConceptPlugin()
    
    ob_concepts = ob_plugin.extract([feature], context)
    brk_concepts = brk_plugin.extract([feature], context)
    
    assert len(ob_concepts) == 1
    assert len(brk_concepts) == 1
    
    # Both concepts reference the exact same immutable zone
    assert ob_concepts[0].source_features[0].zone_dto is zone
    assert brk_concepts[0].source_features[0].zone_dto is zone

def test_explainability_contracts(context):
    zone = create_mock_zone("z1", "GAP_ZONE", ZoneLifecycleStatus.ACTIVE)
    feature_type = FeatureType(id="ZONE_FEATURE", name="Zone Feature", family="SPATIAL")
    feature = ZoneFeature(
        context=context, feature_id="", feature_type=feature_type, version=1, 
        quality=1.0, confidence=1.0, produced_at=datetime.now(timezone.utc),
        zone_dto=zone
    )
    
    plugin = FVGConceptPlugin()
    concept = plugin.extract([feature], context)[0]
    
    # Assert Explainability
    assert concept.semantic_evidence is not None
    assert "imbalance" in concept.semantic_evidence.criteria_met
    assert concept.semantic_evidence.supporting_zone_id == "z1"
    assert concept.semantic_evidence.detector_version == "1.0.0"
    
    assert concept.concept_id.capability_id == "CAP-FVG-01"
    assert concept.concept_id.ontology_id == "ONT-001"

def test_replay_determinism_hash(context):
    zone = create_mock_zone("z1", "GAP_ZONE", ZoneLifecycleStatus.ACTIVE)
    feature_type = FeatureType(id="ZONE_FEATURE", name="Zone Feature", family="SPATIAL")
    feature = ZoneFeature(
        context=context, feature_id="", feature_type=feature_type, version=1, 
        quality=1.0, confidence=1.0, produced_at=datetime.now(timezone.utc),
        zone_dto=zone
    )
    
    plugin = FVGConceptPlugin()
    concept1 = plugin.extract([feature], context)[0]
    concept1.freeze()
    hash1 = concept1.lineage_hash
    
    # Re-extracting from the same inputs must yield the exact same hash
    concept2 = plugin.extract([feature], context)[0]
    concept2.freeze()
    hash2 = concept2.lineage_hash
    
    assert hash1 == hash2
