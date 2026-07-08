import pytest
import time
import os
import yaml
import tracemalloc
from datetime import datetime, timezone
from Backend.platforms.platform8_analysis.frameworks.zone_engines import (
    RegistryResolver, OverlapEngine, MergeEngine, SplitEngine, LifecycleEngine
)
from Backend.shared_domain.contracts.zones.zone_dtos import (
    ZoneDTO, ZoneIdentityDTO, ZoneGeometryDTO, ZoneMetadataDTO, ZoneLifecycleStatus
)
from Backend.platforms.platform8_analysis.frameworks.zone_index import ListZoneIndex

@pytest.fixture
def registry_data():
    registry_path = os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "Docs", "Governance", "registry", "zone_registry.yaml"
    )
    with open(registry_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    state_path = os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "Docs", "Governance", "registry", "zone_state_machine_registry.yaml"
    )
    with open(state_path, 'r', encoding='utf-8') as f:
        state_data = yaml.safe_load(f)
        data["lifecycle"] = state_data.get("zone_lifecycle", {})
        
    return data

@pytest.fixture
def resolver(registry_data):
    return RegistryResolver(registry_data)

def create_mock_zone(top: float, bottom: float, status: ZoneLifecycleStatus, z_id: str = "z1", z_type: str = "GAP_ZONE") -> ZoneDTO:
    identity = ZoneIdentityDTO(
        zone_id=z_id,
        zone_version=1,
        previous_version_id=None,
        root_zone_id=z_id,
        zone_type=z_type,
        ontology_id="ONT-001",
        capability_id="CAP-001",
        market="NASDAQ",
        asset_class="Equities",
        exchange="NASDAQ",
        symbol="AAPL",
        timeframe="H1",
        session_id="RTH",
        source_detector="GapZoneDetector",
        registry_version="1.0.0"
    )
    geometry = ZoneGeometryDTO(
        upper_price=top,
        lower_price=bottom
    )
    metadata = ZoneMetadataDTO(
        registry_version="1.0.0",
        fingerprint_hash="abc123hash",
        created_by="mock_test",
        detector="GapZoneDetector",
        latency_ms=0.5,
        confidence_model="volume_weighted",
        freshness_model="time_decay"
    )
    return ZoneDTO(
        identity=identity,
        geometry=geometry,
        metadata=metadata,
        status=status,
        created_at=datetime.now(timezone.utc)
    )

def test_overlap_engine_calculation():
    z1 = create_mock_zone(100.0, 90.0, ZoneLifecycleStatus.ACTIVE)
    z2 = create_mock_zone(95.0, 85.0, ZoneLifecycleStatus.ACTIVE)
    
    overlap = OverlapEngine.calculate_overlap_percentage(z1, z2)
    assert overlap == 0.5

def test_merge_engine_success(resolver):
    merge_engine = MergeEngine(resolver)
    z1 = create_mock_zone(100.0, 90.0, ZoneLifecycleStatus.ACTIVE, z_id="z1")
    z2 = create_mock_zone(95.0, 85.0, ZoneLifecycleStatus.ACTIVE, z_id="z2")
    
    merged = merge_engine.attempt_merge(z1, z2)
    assert merged is not None
    assert merged.geometry.upper_price == 100.0
    assert merged.geometry.lower_price == 85.0
    assert "z2" in merged.lineage_ids

def test_merge_engine_failure_blocked_by_policy(resolver):
    merge_engine = MergeEngine(resolver)
    z1 = create_mock_zone(100.0, 90.0, ZoneLifecycleStatus.ACTIVE, z_type="BLOCK_ZONE")
    z2 = create_mock_zone(95.0, 85.0, ZoneLifecycleStatus.ACTIVE, z_type="BLOCK_ZONE")
    
    merged = merge_engine.attempt_merge(z1, z2)
    assert merged is None

def test_split_engine(resolver):
    split_engine = SplitEngine(resolver)
    z1 = create_mock_zone(100.0, 90.0, ZoneLifecycleStatus.ACTIVE, z_type="BLOCK_ZONE")
    
    splits = split_engine.attempt_split(z1, 95.0)
    assert len(splits) == 2
    assert splits[0].geometry.upper_price == 100.0
    assert splits[0].geometry.lower_price == 95.0
    assert splits[1].geometry.upper_price == 95.0
    assert splits[1].geometry.lower_price == 90.0

def test_lifecycle_engine(resolver):
    lifecycle_engine = LifecycleEngine(resolver)
    z1 = create_mock_zone(100.0, 90.0, ZoneLifecycleStatus.DETECTED)
    
    z2 = lifecycle_engine.transition(z1, "str.zone.confirm")
    assert z2.status == ZoneLifecycleStatus.CONFIRMED
    
    z3 = lifecycle_engine.transition(z2, "str.zone.activate")
    assert z3.status == ZoneLifecycleStatus.ACTIVE

def test_performance_memory_bounds():
    tracemalloc.start()
    index = ListZoneIndex()
    
    start_insert = time.time()
    for i in range(10000):
        z = create_mock_zone(100.0 + i, 90.0 + i, ZoneLifecycleStatus.ACTIVE, z_id=f"z_{i}")
        index.insert(z)
    end_insert = time.time()
    
    insert_latency = end_insert - start_insert
    assert len(index) == 10000
    assert insert_latency < 5.0
    
    start_query = time.time()
    results = index.find_overlapping(1500.0, 1000.0)
    end_query = time.time()
    
    query_latency = end_query - start_query
    assert len(results) > 0
    assert query_latency < 0.5
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Optional print for CI/CD artifact capturing
    print(f"Metrics | 10k Zones | Latency Insert: {insert_latency:.3f}s | Latency Query: {query_latency:.3f}s | Peak Memory: {peak / 10**6:.2f} MB")
