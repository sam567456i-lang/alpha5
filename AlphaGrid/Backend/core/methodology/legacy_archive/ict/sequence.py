import uuid
from typing import List
from Backend.core.methodology.narrative_node import NarrativeNode, NarrativeSequenceNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage
from Backend.core.methodology.legacy_archive.ict.policies.sequence_policy import ICTSequencePolicy

class ICTSequenceEngine:
    """
    Evaluates ordered collections of NarrativeNodes against ICT temporal models (e.g., AMD, Judas Swing).
    """
    def __init__(self, policy: ICTSequencePolicy = None):
        self.policy = policy or ICTSequencePolicy()
        
    def evaluate(self, nodes_in_chronological_order: List[NarrativeNode]) -> List[NarrativeSequenceNode]:
        sequences = []
        
        for config in self.policy.configurations:
            if self._matches_sequence(nodes_in_chronological_order, config):
                seq = NarrativeSequenceNode(
                    node_id=f"seq_{uuid.uuid4().hex[:8]}",
                    identity=None,
                    concept_type=NarrativeNodeType.NARRATIVE_SEQUENCE,
                    concept_name=f"{config.name} Sequence",
                    stage=NarrativeStage.EXECUTION, # Usually evaluated late in the lifecycle
                    sequence_type=config.name,
                    ordered_narrative_ids=[n.node_id for n in nodes_in_chronological_order],
                    producer_plugin="ICTPlugin",
                    producer_policy=config.name
                )
                sequences.append(seq)
                
        return sequences

    def _matches_sequence(self, nodes: List[NarrativeNode], config) -> bool:
        """
        Simple greedy matcher: Do the nodes in the list contain the required sequence in order?
        """
        req_idx = 0
        reqs = config.required_nodes_in_order
        
        if not reqs:
            return False
            
        for node in nodes:
            current_req = reqs[req_idx]
            
            # Check if this node satisfies the current requirement
            if node.concept_type == current_req.concept_type:
                # Check keywords if any are specified
                if not current_req.concept_name_keywords or any(kw.lower() in node.concept_name.lower() for kw in current_req.concept_name_keywords):
                    req_idx += 1
                    if req_idx == len(reqs):
                        return True
                        
        return False
