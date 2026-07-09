from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass(frozen=True)
class StructureNode:
    node_id: str
    node_type: str  # e.g., 'SWING', 'IMBALANCE'
    reference_id: str
    parent_ids: List[str]
    child_ids: List[str]
    classification: str
    depth: int

@dataclass(frozen=True)
class StructureEdge:
    source_id: str
    target_id: str
    edge_type: str  # e.g., 'PARENT', 'SUCCESSOR', 'INVALIDATES', 'SUPERSEDES', 'CONTAINS', 'DERIVED_FROM'

@dataclass(frozen=True)
class StructureGraphDTO:
    """A geometric graph representing the topography of structural elements."""
    nodes: Dict[str, StructureNode] = field(default_factory=dict)
    edges: List[StructureEdge] = field(default_factory=list)
    active_leg_id: Optional[str] = None
    root_node_ids: List[str] = field(default_factory=list)
    graph_schema_version: str = "1.0.0"
    graph_version: int = 1
    graph_checksum: str = "none"
