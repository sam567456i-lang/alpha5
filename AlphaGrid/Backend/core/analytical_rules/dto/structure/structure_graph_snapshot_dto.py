from dataclasses import dataclass
from typing import Dict, Any
from Backend.core.analytical_rules.dto.structure.structure_graph_dto import StructureGraphDTO

@dataclass(frozen=True)
class StructureGraphSnapshotDTO:
    """Read-only boundary for downstream consumers (Platform 10/11) to inspect the structure graph."""
    snapshot_id: str
    timestamp: str
    graph: StructureGraphDTO
    metadata: Dict[str, Any]
