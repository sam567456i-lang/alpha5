from typing import List, Dict, Any, Set
import networkx as nx

from Backend.price_geometry.graph.geometry_graph import GeometryGraph
from Backend.price_geometry.objects import GeometryObject

class GeometryProvenance:
    """
    Traces any arbitrary geometry object back to its root dataset objects.
    """
    def __init__(self, graph: GeometryGraph):
        self.graph = graph
        
    def trace_origin(self, obj_id: str) -> List[GeometryObject]:
        """
        Returns all root nodes (Swings) that ultimately formed the given object.
        Traverses the 'ParentOf' edges backwards.
        """
        if not self.graph._graph.has_node(obj_id):
            return []
            
        # We want all ancestors in a directed graph where edges point Parent -> Child.
        # networkx ancestors() returns all nodes having a path to the target node.
        ancestor_ids = nx.ancestors(self.graph._graph, obj_id)
        
        ancestors = []
        for aid in ancestor_ids:
            ancestors.append(self.graph.get_node(aid))
            
        # Filter down to only Root nodes (in-degree 0), which are usually Swings
        roots = []
        for aid in ancestor_ids:
            if self.graph._graph.in_degree(aid) == 0:
                roots.append(self.graph.get_node(aid))
                
        return sorted(roots, key=lambda x: x.timestamp)
        
    def audit_trail(self, obj_id: str) -> Dict[str, Any]:
        """
        Returns a complete audit JSON of how an object was formed, including fingerprints.
        """
        obj = self.graph.get_node(obj_id)
        if not obj:
            return {"error": "Object not found"}
            
        trail = {
            "target_id": obj_id,
            "target_fingerprint": obj.fingerprint,
            "target_type": obj.__class__.__name__,
            "parents": []
        }
        
        for pid in obj.parent_ids:
            parent_trail = self.audit_trail(pid)
            trail["parents"].append(parent_trail)
            
        return trail
