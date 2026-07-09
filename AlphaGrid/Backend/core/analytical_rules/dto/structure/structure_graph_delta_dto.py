from dataclasses import dataclass, field
from typing import Dict, Any, List
from Backend.core.analytical_rules.dto.structure.structure_graph_dto import StructureNode, StructureEdge

@dataclass(frozen=True)
class StructureGraphDeltaDTO:
    """Represents a diff between two graph snapshots."""
    added_nodes: List[StructureNode] = field(default_factory=list)
    removed_node_ids: List[str] = field(default_factory=list)
    updated_nodes: List[StructureNode] = field(default_factory=list)
    
    added_edges: List[StructureEdge] = field(default_factory=list)
    removed_edges: List[StructureEdge] = field(default_factory=list)
    
    metadata_changes: Dict[str, Any] = field(default_factory=dict)
