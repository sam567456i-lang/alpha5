import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from Backend.core.methodology.narrative_node import NarrativeNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, MethodologyType

@dataclass
class NarrativeGraph:
    """
    Independent graph containing subjective methodology narratives.
    Does not duplicate objective evidence, only references it via IDs.
    """
    methodology: MethodologyType
    nodes: Dict[str, NarrativeNode] = field(default_factory=dict)
    
    def add_node(self, node: NarrativeNode) -> None:
        """Register a new subjective interpretation."""
        node_methodology = node.identity.methodology if node.identity else None
        if node_methodology != self.methodology:
            raise ValueError(f"Node methodology {node_methodology} does not match graph {self.methodology}")
        self.nodes[node.node_id] = node
        
    def find(self, node_id: str) -> Optional[NarrativeNode]:
        """Retrieve a specific narrative by ID."""
        return self.nodes.get(node_id)
        
    def filter_by_type(self, concept_type: NarrativeNodeType) -> List[NarrativeNode]:
        """Find all nodes of a specific methodology concept."""
        return [n for n in self.nodes.values() if n.concept_type == concept_type]
        
    def filter_by_evidence(self, evidence_id: str) -> List[NarrativeNode]:
        """Find all narratives referencing a specific piece of objective evidence."""
        return [n for n in self.nodes.values() if evidence_id in n.supporting_evidence_ids]
        
    def _hash_dict(self, d: Dict[str, Any]) -> str:
        # Sort keys to ensure deterministic hashing
        serialized = json.dumps(list(sorted(d.keys())))
        return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

    def checksum(self) -> str:
        """
        Calculates a deterministic hash representing the exact narrative state.
        Used for replay certification.
        """
        return self._hash_dict(self.nodes)

    def validate(self) -> Dict[str, List[str]]:
        """
        Validates graph integrity (e.g., checking for nodes with missing mandatory metadata).
        """
        issues = {"invalid_provenance": [], "missing_type": []}
        for node_id, node in self.nodes.items():
            if not node.producer_plugin:
                issues["invalid_provenance"].append(node_id)
            if not node.concept_type:
                issues["missing_type"].append(node_id)
        return issues
        
    def statistics(self) -> Dict[str, Any]:
        """
        Exposes internal stats for benchmarking.
        """
        stats = {"total_nodes": len(self.nodes)}
        for type_enum in NarrativeNodeType:
            stats[f"count_{type_enum.value}"] = len(self.filter_by_type(type_enum))
        return stats

    # --- Narrative Query API ---
    
    def context(self) -> List[NarrativeNode]:
        """Returns the centralized Market Context nodes."""
        return self.filter_by_type(NarrativeNodeType.MARKET_CONTEXT)
        
    def bias(self) -> List[NarrativeNode]:
        """Returns all Market Bias nodes in this methodology's narrative."""
        return self.filter_by_type(NarrativeNodeType.BIAS)
        
    def poi(self) -> List[NarrativeNode]:
        """Returns all Point of Interest (POI) nodes selected by this methodology."""
        return self.filter_by_type(NarrativeNodeType.POI)
        
    def targets(self) -> List[NarrativeNode]:
        """Returns all designated Liquidity Targets."""
        return self.filter_by_type(NarrativeNodeType.LIQUIDITY_TARGET)
        
    def structure(self) -> List[NarrativeNode]:
        """Returns structure narratives (e.g., CHOCH, BOS, MSS)."""
        return self.filter_by_type(NarrativeNodeType.STRUCTURE_NARRATIVE)
        
    def setup(self) -> List[NarrativeNode]:
        """Returns all aggregated setup configurations."""
        return self.filter_by_type(NarrativeNodeType.SETUP)
        
    def execution(self) -> List[NarrativeNode]:
        """Returns all execution plans/triggers."""
        return self.filter_by_type(NarrativeNodeType.EXECUTION)
        
    def entry(self) -> List[NarrativeNode]:
        """Returns all actionable Entry triggers."""
        return self.filter_by_type(NarrativeNodeType.ENTRY)
        
    def invalidation(self) -> List[NarrativeNode]:
        """Returns all Invalidation criteria narratives."""
        return self.filter_by_type(NarrativeNodeType.INVALIDATION)
        
    def trade(self) -> List[NarrativeNode]:
        """Returns all formalized trade nodes."""
        # For future expansion
        return []

        
    def explain(self, node_id: str) -> Dict[str, Any]:
        """
        Provides a deep explanation of a narrative node by tracing its 
        supporting evidence and supporting narratives.
        """
        node = self.find(node_id)
        if not node:
            return {"error": "Node not found."}
            
        return {
            "narrative": node.concept_name,
            "type": node.concept_type.value,
            "methodology": node.methodology.value,
            "confidence_inputs": node.confidence_inputs,
            "supporting_evidence_ids": node.supporting_evidence_ids,
            "supporting_narratives": [
                self.explain(sub_id) for sub_id in node.supporting_narrative_ids if sub_id in self.nodes
            ]
        }
        
    def explain_path(self, root_id: str, target_evidence_id: str) -> List[str]:
        """
        Traces the linear dependency path from a subjective narrative root down
        to a specific objective evidence ID.
        Returns the path of node IDs, e.g., ["entry_1", "poi_1", "evidence_5"].
        Returns empty list if no path exists.
        """
        path = []
        
        def dfs(current_id: str) -> bool:
            path.append(current_id)
            node = self.find(current_id)
            if not node:
                path.pop()
                return False
                
            if target_evidence_id in node.supporting_evidence_ids:
                path.append(target_evidence_id)
                return True
                
            for supp_id in node.supporting_narrative_ids:
                if dfs(supp_id):
                    return True
                    
            path.pop()
            return False
            
        if dfs(root_id):
            return path
        return []


