import pytest
import pandas as pd
from datetime import datetime
from Backend.price_geometry.geometry_engine import GeometryEngineOrchestrator
from Backend.price_geometry.cache import GeometryCache
from Backend.price_geometry.objects import LifecycleState, Structure

class MockContext:
    def __init__(self):
        self.geometry_cache = GeometryCache()
        self.symbol = "BTCUSDT"
        self.timeframe = "1H"
        self.dataset_id = "test"

def test_dag_topological_sort():
    """Validates that engines execute in the correct DAG sequence."""
    orchestrator = GeometryEngineOrchestrator()
    sequence = orchestrator.engine_sequence
    print(f"Sequence: {sequence}")
    
    # OrderBlockEngine depends on StructureEngine and SwingEngine
    ob_index = sequence.index("OrderBlockEngine")
    struct_index = sequence.index("StructureEngine")
    swing_index = sequence.index("SwingEngine")
    
    assert ob_index > struct_index, "OrderBlockEngine must execute AFTER StructureEngine"
    assert ob_index > swing_index, "OrderBlockEngine must execute AFTER SwingEngine"

def test_geometry_immutability():
    """Validates the evolve() method creates a new instance and bumps version."""
    s1 = Structure(
        id="BOS-1",
        version="v1.0.0",
        dataset_id="test",
        symbol="BTCUSDT",
        timeframe="1H",
        timestamp=datetime.utcnow(),
        price=100.0,
        structure_type="BOS",
        lifecycle_state=LifecycleState.DETECTED
    )
    
    s2 = s1.evolve(lifecycle_state=LifecycleState.CONFIRMED)
    
    # Object identity should differ
    assert id(s1) != id(s2)
    # Original should be untouched
    assert s1.lifecycle_state == LifecycleState.DETECTED
    # New should have new state
    assert s2.lifecycle_state == LifecycleState.CONFIRMED
    # Version should have bumped
    assert s2.version == "v1.0.0-1"
    
    s3 = s2.evolve(lifecycle_state=LifecycleState.BROKEN)
    assert s3.version == "v1.0.0-2"
