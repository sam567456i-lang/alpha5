import pytest
from Backend.core.methodology.multi_timeframe_graph import MultiTimeframeEvidenceGraph
from Backend.core.methodology.narrative_node import MarketContextNode, LiquidityTargetNode
from Backend.core.methodology.ict.liquidity import ICTLiquidityModule
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage

def test_ict_liquidity_evaluation():
    # Setup
    mtf = MultiTimeframeEvidenceGraph()
    context = MarketContextNode(
        node_id="ctx_1",
        identity=None, # In a real scenario, would be NarrativeIdentity
        concept_type=NarrativeNodeType.MARKET_CONTEXT,
        concept_name="HTF Bullish Context",
        stage=NarrativeStage.CONTEXT,
        bias_node_id="bias_1"
    )
    
    module = ICTLiquidityModule()
    candidates, targets = module.evaluate_targets(mtf, context)
    
    # Assertions
    assert len(candidates) == 3
    assert len(targets) == 3
    assert all(isinstance(t, LiquidityTargetNode) for t in targets)
    assert all(t.stage == NarrativeStage.TARGETING for t in targets)
    
    # Priority sorting check (descending) by candidates
    scores = [c.priority_score for c in candidates]
    assert scores == sorted(scores, reverse=True)
    
    # Top candidate should be 1D BSL due to htf and structure alignment
    top_cand = candidates[0]
    assert "BSL" in top_cand.concept_name
    assert top_cand.ranking_components["htf_alignment"] == 30
    assert top_cand.ranking_components["structure_alignment"] == 30
    assert top_cand.priority_score == 85
    
    # Check targets link back
    top_target = targets[0]
    assert top_target.candidate_node_id == top_cand.node_id

