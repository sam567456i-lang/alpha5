import pytest
from Backend.core.analytical_rules.capabilities.evidence_graph import EvidenceGraph
from Backend.core.methodology.multi_timeframe_graph import MultiTimeframeEvidenceGraph
from Backend.core.methodology.ict.context import ICTContextModule
from Backend.core.methodology.narrative_node import BiasNode, POINode
from Backend.core.methodology.narrative_types import NarrativeNodeType

def test_ict_bias_evaluation():
    # Setup MTF Graph with 4H and 1D graphs
    mtf_graph = MultiTimeframeEvidenceGraph()
    mtf_graph.add_timeframe("4H", EvidenceGraph())
    mtf_graph.add_timeframe("1D", EvidenceGraph())
    
    # Initialize Context Module
    context_module = ICTContextModule(htf_intervals=["4H", "1D"])
    
    # Evaluate Bias
    bias_node = context_module.evaluate_bias(mtf_graph)
    
    # Assertions
    assert isinstance(bias_node, BiasNode)
    assert bias_node.concept_type == NarrativeNodeType.BIAS
    assert bias_node.direction in ["BULLISH", "BEARISH", "NEUTRAL"]
    
    # Verify the bias explicitly tracked its evidence backing
    assert bias_node.supported_by_structure is True
    assert bias_node.supported_by_liquidity is True
    assert len(bias_node.supporting_evidence_ids) > 0
    
def test_ict_poi_evaluation():
    mtf_graph = MultiTimeframeEvidenceGraph()
    mtf_graph.add_timeframe("4H", EvidenceGraph())
    
    context_module = ICTContextModule(htf_intervals=["4H"])
    
    pois = context_module.evaluate_pois(mtf_graph)
    
    assert len(pois) > 0
    poi_node = pois[0]
    
    assert isinstance(poi_node, POINode)
    assert poi_node.concept_type == NarrativeNodeType.POI
    assert poi_node.poi_type == "FVG"
    assert len(poi_node.supporting_evidence_ids) > 0
