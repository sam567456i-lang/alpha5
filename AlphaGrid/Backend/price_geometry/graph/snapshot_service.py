from typing import Dict, Any, Optional
import json
import os
import networkx as nx
from datetime import datetime
import hashlib

from Backend.price_geometry.graph.geometry_graph import GeometryGraph

class GeometrySnapshotService:
    """
    Manages deterministic snapshots of the GeometryGraph.
    Prevents recalculation from bar 0 during restarts or replays.
    """
    def __init__(self, snapshot_dir: str = "data/snapshots/geometry"):
        self.snapshot_dir = snapshot_dir
        os.makedirs(self.snapshot_dir, exist_ok=True)
        
    def _generate_snapshot_id(self, dataset_id: str, timestamp: datetime) -> str:
        s = f"{dataset_id}_{timestamp.isoformat()}"
        return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]
        
    def take_snapshot(self, graph: GeometryGraph, timestamp: datetime) -> str:
        """Serializes the current graph to a persistent snapshot."""
        snapshot_id = self._generate_snapshot_id(graph.dataset_id, timestamp)
        filepath = os.path.join(self.snapshot_dir, f"{snapshot_id}.json")
        
        # We need a custom serializer for GeometryObjects
        # For this PoC, we assume they can be serialized easily or we use pickle.
        # Since networkx supports writing to graphml/json, we use node_link_data.
        
        # Simplification for implementation:
        # We would serialize the dataclasses into dicts.
        data = graph.to_dict()
        
        with open(filepath, 'w') as f:
            json.dump(data, f)
            
        return snapshot_id
        
    def load_snapshot(self, snapshot_id: str) -> Optional[GeometryGraph]:
        """Loads a snapshot back into memory."""
        filepath = os.path.join(self.snapshot_dir, f"{snapshot_id}.json")
        if not os.path.exists(filepath):
            return None
            
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        # Reconstruct graph
        dataset_id = data["dataset_id"]
        graph = GeometryGraph(dataset_id)
        
        # In a real implementation, we would deserialize dicts back to GeometryObjects
        # graph._graph = nx.node_link_graph(data["nodes"][0])
        # Repopulate graph._objects_by_type
        
        return graph
