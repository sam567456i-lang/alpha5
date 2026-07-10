from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class CRL(Enum):
    CRL0_CONCEPT = 0
    CRL1_ARCHITECTURE = 1
    CRL2_SPECIFICATION = 2
    CRL3_PROTOTYPE = 3
    CRL4_IMPLEMENTED = 4
    CRL5_VERIFIED = 5
    CRL6_PRODUCTION_READY = 6
    CRL7_CERTIFIED = 7
    CRL8_FROZEN = 8

@dataclass
class CapabilityNode:
    """The 27-attribute Source of Truth for every capability in AlphaGrid."""
    identity: str
    domain: str
    platform: str
    program: str
    family: str
    engine: str
    rules: List[str] = field(default_factory=list)
    features_produced: List[str] = field(default_factory=list)
    features_consumed: List[str] = field(default_factory=list)
    evidence_produced: List[str] = field(default_factory=list)
    evidence_consumed: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    consumers: List[str] = field(default_factory=list)
    data_requirements: List[str] = field(default_factory=list)
    timeframes: List[str] = field(default_factory=list)
    markets: List[str] = field(default_factory=list)
    asset_classes: List[str] = field(default_factory=list)
    streaming_support: bool = False
    replay_support: bool = True
    computational_cost: str = "Medium"
    parallelizable: bool = False
    crl: CRL = CRL.CRL0_CONCEPT
    version: str = "0.0.0"
    tests: List[str] = field(default_factory=list)
    benchmarks: List[str] = field(default_factory=list)
    certification: Optional[str] = None
    adr: Optional[str] = None
    owner: str = "core_team"

class CapabilityKnowledgeGraph:
    """
    The Master Ontology for AlphaGrid.
    All roadmaps, generators, and validations derive from this graph.
    """
    def __init__(self):
        self._nodes: Dict[str, CapabilityNode] = {}
        
    def add_node(self, node: CapabilityNode):
        if node.identity in self._nodes:
            raise ValueError(f"Capability {node.identity} already exists in the Knowledge Graph.")
        self._nodes[node.identity] = node

    def get_node(self, identity: str) -> Optional[CapabilityNode]:
        return self._nodes.get(identity)

    def get_all_nodes(self) -> List[CapabilityNode]:
        return list(self._nodes.values())
        
    def get_downstream_consumers(self, identity: str) -> List[CapabilityNode]:
        node = self.get_node(identity)
        if not node: return []
        
        # Traverse nodes where this identity is listed in dependencies or evidence_consumed
        consumers = []
        for n in self.get_all_nodes():
            if identity in n.dependencies:
                consumers.append(n)
            # Match produced evidence to consumed evidence
            for evidence in node.evidence_produced:
                if evidence in n.evidence_consumed and n not in consumers:
                    consumers.append(n)
                    
        return consumers
