import uuid
from typing import List, Optional
from Backend.core.methodology.narrative_node import ConfluenceCandidateNode, TradeSetupNode, PDArrayNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage
from Backend.core.methodology.legacy_archive.ict.policies.confluence_policy import ICTConfluencePolicy

class ICTConfluenceEngine:
    """
    Evaluates ConfluenceCandidateNodes against ICTConfluencePolicy to emit TradeSetupNodes.
    """
    def __init__(self, policy: ICTConfluencePolicy = None):
        self.policy = policy or ICTConfluencePolicy()
        
    def evaluate(self, candidates: List[ConfluenceCandidateNode], pd_arrays: List[PDArrayNode]) -> List[TradeSetupNode]:
        setups = []
        
        # Helper to get PDArray by ID
        array_map = {a.node_id: a for a in pd_arrays}
        
        for cand in candidates:
            # Gather arrays in this candidate
            cand_arrays = [array_map[node_id] for node_id in cand.intersecting_narrative_ids if node_id in array_map]
            
            for config in self.policy.configurations:
                if self._matches_config(cand_arrays, config):
                    setup = TradeSetupNode(
                        node_id=f"ts_{uuid.uuid4().hex[:8]}",
                        identity=None,
                        concept_type=NarrativeNodeType.SETUP,
                        concept_name=f"{config.name} Setup",
                        stage=NarrativeStage.SETUP,
                        setup_direction="TBD", # Would be derived from arrays
                        is_active=True,
                        supporting_narrative_ids=[cand.node_id],
                        producer_plugin="ICTPlugin",
                        producer_policy=config.name
                    )
                    setups.append(setup)
                    
        return setups

    def _matches_config(self, arrays: List[PDArrayNode], config) -> bool:
        """
        Simple check: does the candidate contain all the required array types for this config?
        """
        array_types = [a.array_type for a in arrays]
        for req in config.required_pd_arrays:
            if req.array_type in array_types:
                array_types.remove(req.array_type)
            else:
                return False
        return True
