from typing import Dict, Any, List
from Backend.concepts.core.objects import ConceptObject
from Backend.price_geometry.graph.geometry_graph import GeometryGraph
from Backend.price_geometry.graph.provenance import GeometryProvenance

class ConceptProvenance:
    """
    Traces concepts back to their underlying GeometryGraph nodes and ultimately raw dataset bars.
    """
    def __init__(self, geometry_graph: GeometryGraph):
        self.geom_provenance = GeometryProvenance(geometry_graph)
        
    def trace_concept(self, concept: ConceptObject) -> Dict[str, Any]:
        """
        Returns full audit trail for the concept.
        """
        trail: Dict[str, Any] = {
            "concept_id": concept.id,
            "concept_type": concept.concept_type,
            "concept_fingerprint": concept.fingerprint,
            "geometry_dependencies": []
        }
        
        for geom_id in concept.geometry_dependency_ids:
            geom_trail = self.geom_provenance.audit_trail(geom_id)
            trail["geometry_dependencies"].append(geom_trail)
            
        return trail
