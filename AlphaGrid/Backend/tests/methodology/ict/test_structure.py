import pytest
from Backend.core.methodology.multi_timeframe_graph import MultiTimeframeEvidenceGraph
from Backend.core.methodology.narrative_node import MarketContextNode, LiquidityTargetNode, StructureNarrativeNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage
from Backend.core.methodology.ict.structure import ICTStructureModule
import uuid

def test_ict_structure_evaluation():
    # Setup
    mtf = MultiTimeframeEvidenceGraph()
    context = MarketContextNode(
        node_id="ctx_1",
        identity=None,
        concept_type=NarrativeNodeType.MARKET_CONTEXT,
        concept_name="HTF Bullish Context",
        stage=NarrativeStage.CONTEXT,
        bias_node_id="bias_1"
    )
    
    targets = [
        LiquidityTargetNode(
            node_id="target_1",
            identity=None,
            concept_type=NarrativeNodeType.LIQUIDITY_TARGET,
            concept_name="BSL Target",
            stage=NarrativeStage.TARGETING
        )
    ]
    
    module = ICTStructureModule()
    candidates, narratives = module.evaluate_structure(mtf, context, targets)
    
    # Assertions
    assert len(candidates) == 3
    assert len(narratives) == 3
    assert all(isinstance(n, StructureNarrativeNode) for n in narratives)
    assert all(n.stage == NarrativeStage.STRUCTURE for n in narratives)
    assert all(n.concept_type == NarrativeNodeType.STRUCTURE_NARRATIVE for n in narratives)
    
    # Check BOS (Continuation)
    bos = [n for n in narratives if n.structure_label == "BOS"]
    assert len(bos) == 1
    
    # Check CHOCH (Reversal)
    choch = [n for n in narratives if n.structure_label == "CHOCH"]
    assert len(choch) == 1
    
    # Check MSS (Shift)
    mss = [n for n in narratives if n.structure_label == "MSS"]
    assert len(mss) == 1
    assert mss[0].candidate_node_id != ""
