from typing import Dict, List, Optional
from dataclasses import dataclass
from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO

@dataclass
class VersionNode:
    evidence_id: str
    evidence: EvidenceDTO
    parents: List[str]
    children: List[str]

class EvidenceVersionGraph:
    """First-class lineage graph tracking branching updates to Evidence."""
    def __init__(self):
        self.nodes: Dict[str, VersionNode] = {}
        
    def add_evidence(self, evidence: EvidenceDTO, parent_ids: List[str] = None):
        if parent_ids is None: parent_ids = []
        node = VersionNode(
            evidence_id=evidence.identity.id,
            evidence=evidence,
            parents=parent_ids,
            children=[]
        )
        self.nodes[node.evidence_id] = node
        
        # Link parents to this new child
        for parent_id in parent_ids:
            if parent_id in self.nodes:
                self.nodes[parent_id].children.append(node.evidence_id)
                
    def get_lineage(self, evidence_id: str) -> List[str]:
        """Returns the full chain of descendants for a specific piece of evidence."""
        lineage = []
        node = self.nodes.get(evidence_id)
        if node:
            lineage.append(node.evidence_id)
            for child in node.children:
                lineage.extend(self.get_lineage(child))
        return lineage
