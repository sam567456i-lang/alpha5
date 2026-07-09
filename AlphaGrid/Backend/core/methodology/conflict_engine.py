import uuid
from typing import List
from Backend.core.methodology.narrative_node import NarrativeNode, MarketContextNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage

class ConflictEngine:
    """
    Scans a set of narrative nodes for logical conflicts (both intra-methodology and inter-methodology).
    """
    
    def detect_conflicts(self, nodes: List[NarrativeNode]) -> List[NarrativeNode]:
        conflicts = []
        conflicts.extend(self._detect_market_context_conflicts(nodes))
        # Additional conflict detectors (e.g. Structure vs Liquidity) can be added here
        return conflicts
        
    def _detect_market_context_conflicts(self, nodes: List[NarrativeNode]) -> List[NarrativeNode]:
        conflicts = []
        context_nodes = [n for n in nodes if isinstance(n, MarketContextNode)]
        
        # Group by timeframe or just general bias check
        bullish = [n for n in context_nodes if "Bullish" in n.concept_name]
        bearish = [n for n in context_nodes if "Bearish" in n.concept_name]
        
        if bullish and bearish:
            # We have a conflict
            conflicting_ids = [n.node_id for n in bullish] + [n.node_id for n in bearish]
            
            conflict_node = NarrativeNode(
                node_id=f"conf_{uuid.uuid4().hex[:8]}",
                identity=None,
                concept_type=NarrativeNodeType.CONFLICT,
                concept_name="Market Context Conflict",
                stage=NarrativeStage.CONTEXT,
                supporting_narrative_ids=conflicting_ids,
                producer_plugin="ConflictEngine"
            )
            conflicts.append(conflict_node)
            
        return conflicts
