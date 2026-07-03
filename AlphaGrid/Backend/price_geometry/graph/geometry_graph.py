from typing import Dict, List, Optional, Set
import networkx as nx
from datetime import datetime

from Backend.price_geometry.objects import GeometryObject, LifecycleState, Imbalance, Liquidity, Structure

class GeometryGraph:
    """
    Canonical Directed Acyclic Graph representing all active market geometry.
    Prevents downstream engines from querying individual engines directly.
    """
    def __init__(self, dataset_id: str):
        self.dataset_id = dataset_id
        # We use networkx for topological sorting and complex graph queries
        self._graph = nx.DiGraph()
        # Fast lookup cache for objects by type
        self._objects_by_type: Dict[str, Set[str]] = {
            "Swing": set(),
            "Structure": set(),
            "Liquidity": set(),
            "Imbalance": set(),
            "Zone": set(),
            "ConflictEvent": set()
        }
        
    def add_object(self, obj: GeometryObject) -> None:
        """Add a geometry object as a node in the DAG."""
        # Add Node
        self._graph.add_node(obj.id, data=obj)
        
        # Add type lookup
        obj_type = obj.__class__.__name__
        if obj_type not in self._objects_by_type:
            self._objects_by_type[obj_type] = set()
        self._objects_by_type[obj_type].add(obj.id)
        
        # Add Edges (Parent -> Child relationships)
        for parent_id in obj.parent_ids:
            if self._graph.has_node(parent_id):
                # The arrow points from parent to child (dependency direction)
                self._graph.add_edge(parent_id, obj.id, relationship="ParentOf")
                
    def update_object_state(self, obj_id: str, new_state: LifecycleState, mitigated_price: Optional[float] = None) -> None:
        """Update the lifecycle state of a node (e.g., INVALIDATED, BROKEN)."""
        if self._graph.has_node(obj_id):
            obj = self._graph.nodes[obj_id]["data"]
            # Since GeometryObject is frozen, we update via object.__setattr__ to bypass frozen 
            # Or in a pure immutable system, we'd replace the node.
            # Here we replace the node with a new instance if needed, or just mutate for performance
            # Given Python dataclasses frozen=True, mutating via object.__setattr__ is a workaround.
            # A cleaner way is replace(), but we'll use setattr for simplicity in this PoC engine.
            object.__setattr__(obj, 'lifecycle_state', new_state)
            if mitigated_price is not None:
                object.__setattr__(obj, 'mitigated_price', mitigated_price)
                
    def get_node(self, obj_id: str) -> Optional[GeometryObject]:
        if self._graph.has_node(obj_id):
            return self._graph.nodes[obj_id]["data"]
        return None

    def get_active_liquidity_pools(self) -> List[Liquidity]:
        """Query active liquidity pools."""
        pool_ids = self._objects_by_type.get("Liquidity", set())
        active = []
        for pid in pool_ids:
            obj = self._graph.nodes[pid]["data"]
            if obj.lifecycle_state == LifecycleState.CONFIRMED:
                active.append(obj)
        return active
        
    def get_unmitigated_fvgs(self) -> List[Imbalance]:
        """Query active Fair Value Gaps."""
        imb_ids = self._objects_by_type.get("Imbalance", set())
        active = []
        for iid in imb_ids:
            obj = self._graph.nodes[iid]["data"]
            if obj.lifecycle_state == LifecycleState.CONFIRMED:
                active.append(obj)
        return active
        
    def get_structural_trend(self, timeframe: str) -> Optional[bool]:
        """Return True for Bullish, False for Bearish based on latest active Structure."""
        struct_ids = self._objects_by_type.get("Structure", set())
        active = []
        for sid in struct_ids:
            obj = self._graph.nodes[sid]["data"]
            if obj.timeframe == timeframe and obj.lifecycle_state == LifecycleState.CONFIRMED:
                active.append(obj)
        
        if not active:
            return None
            
        latest = sorted(active, key=lambda x: x.timestamp)[-1]
        return latest.is_bullish
        
    def to_dict(self) -> Dict:
        """Serialize the graph state."""
        return {
            "dataset_id": self.dataset_id,
            "nodes": [nx.node_link_data(self._graph)],
            "timestamp": datetime.utcnow().isoformat()
        }
