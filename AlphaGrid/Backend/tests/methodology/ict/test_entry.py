import pytest
from Backend.core.methodology.multi_timeframe_graph import MultiTimeframeEvidenceGraph
from Backend.core.methodology.narrative_node import MarketContextNode, LiquidityTargetNode, StructureNarrativeNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage
from Backend.core.methodology.ict.entry import ICTEntryModule

def test_ict_entry_evaluation():
    # Setup
    mtf = MultiTimeframeEvidenceGraph()
    context = MarketContextNode(
        node_id="ctx_1",
        identity=None,
        concept_type=NarrativeNodeType.MARKET_CONTEXT,
        concept_name="Bullish Context",
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
    
    structure = [
        StructureNarrativeNode(
            node_id="struct_1",
            identity=None,
            concept_type=NarrativeNodeType.STRUCTURE_NARRATIVE,
            concept_name="MSS",
            stage=NarrativeStage.STRUCTURE,
            structure_label="MSS",
            candidate_node_id="cand_1"
        )
    ]
    
    module = ICTEntryModule()
    ranges, arrays, setups, candidates, entries = module.evaluate_entries(mtf, context, targets, structure)
    
    # Assertions
    assert all(n.stage in [NarrativeStage.SETUP, NarrativeStage.EXECUTION] for n in ranges + arrays + setups + candidates + entries)
    assert len(ranges) == 1
    assert ranges[0].concept_name == "Current Dealing Range"
    assert ranges[0].range_high_price_cached == 1.1050
    assert ranges[0].range_low_price_cached == 1.1000
    
    assert len(arrays) == 1
    assert arrays[0].array_type == "FVG"
    assert arrays[0].classification == "Discount"
    assert arrays[0].dealing_range_node_id == ranges[0].node_id
    
    assert len(setups) == 1
    assert setups[0].setup_direction == "BULLISH"
    assert ranges[0].node_id in setups[0].supporting_narrative_ids
    assert arrays[0].node_id in setups[0].supporting_narrative_ids
    
    assert len(candidates) == 1
    assert candidates[0].fib_level == 0.705
    assert candidates[0].stop_loss_price == 1.1000
    assert candidates[0].target_price == 1.1050
    
    assert len(entries) == 1
    assert entries[0].entry_type == "OTE"
    assert entries[0].candidate_node_id == candidates[0].node_id
