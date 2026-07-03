import pytest
import os
import shutil
from datetime import datetime
from Backend.price_geometry.graph.geometry_graph import GeometryGraph
from Backend.price_geometry.graph.snapshot_service import GeometrySnapshotService

def test_snapshot_service():
    snapshot_dir = "tests/temp_snapshots"
    service = GeometrySnapshotService(snapshot_dir=snapshot_dir)
    
    graph = GeometryGraph("dataset_xyz")
    # For this test we will just serialize an empty graph
    
    ts = datetime(2026, 1, 1)
    snapshot_id = service.take_snapshot(graph, ts)
    
    loaded_graph = service.load_snapshot(snapshot_id)
    assert loaded_graph is not None
    assert loaded_graph.dataset_id == "dataset_xyz"
    
    # Cleanup
    shutil.rmtree(snapshot_dir)
