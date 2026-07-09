import pytest
from Backend.core.analytical_rules.capabilities.evidence_graph import EvidenceGraph
from Backend.core.methodology.multi_timeframe_graph import MultiTimeframeEvidenceGraph
from Backend.core.methodology.narrative_node import NarrativeNode, NarrativeIdentity
from Backend.core.methodology.narrative_graph import NarrativeGraph
from Backend.core.methodology.narrative_types import NarrativeNodeType, MethodologyType
from Backend.core.methodology.plugin_interface import MethodologyPlugin

class StubICTPlugin(MethodologyPlugin):
    @property
    def methodology_type(self) -> MethodologyType:
        return MethodologyType.ICT
        
    @property
    def version(self) -> str:
        return "1.0"
        
    def execute(self, mtf_graph: MultiTimeframeEvidenceGraph, context=None) -> NarrativeGraph:
        graph = NarrativeGraph(methodology=self.methodology_type)
        
        # Stub logic: emit a BIAS node based on finding evidence in 4H
        h4_graph = mtf_graph.timeframe("4H")
        if h4_graph:
            bias_node = NarrativeNode(
                node_id="bias_1",
                identity=NarrativeIdentity(
                    methodology=self.methodology_type,
                    plugin_version="1.0",
                    rule_version="1.0",
                    graph_namespace="main",
                    timeframe="4H",
                    creation_sequence=1
                ),
                concept_type=NarrativeNodeType.BIAS,
                concept_name="Bullish Bias",
                supporting_evidence_ids=["stub_evidence_1"]
            )
            graph.add_node(bias_node)
            
        return graph

def test_multi_timeframe_graph():
    mtf = MultiTimeframeEvidenceGraph()
    mtf.add_timeframe("4H", EvidenceGraph())
    
    assert mtf.timeframe("4H") is not None
    assert mtf.timeframe("1H") is None
    assert "4H" in mtf.available_timeframes()

def test_narrative_graph():
    ng = NarrativeGraph(methodology=MethodologyType.ICT)
    node = NarrativeNode(
        node_id="n1",
        identity=NarrativeIdentity(
            methodology=MethodologyType.ICT,
            plugin_version="1.0",
            rule_version="1.0",
            graph_namespace="main",
            timeframe="4H",
            creation_sequence=1
        ),
        concept_type=NarrativeNodeType.POI,
        concept_name="Order Block POI",
        supporting_evidence_ids=["ev_1"]
    )
    ng.add_node(node)
    
    assert ng.find("n1") == node
    assert len(ng.filter_by_type(NarrativeNodeType.POI)) == 1
    assert len(ng.filter_by_evidence("ev_1")) == 1

def test_plugin_execution():
    mtf = MultiTimeframeEvidenceGraph()
    mtf.add_timeframe("4H", EvidenceGraph())
    
    plugin = StubICTPlugin()
    narrative_graph = plugin.execute(mtf)
    
    assert narrative_graph.methodology == MethodologyType.ICT
    bias_nodes = narrative_graph.filter_by_type(NarrativeNodeType.BIAS)
    assert len(bias_nodes) == 1
    assert bias_nodes[0].concept_name == "Bullish Bias"
    assert bias_nodes[0].identity.plugin_version == "1.0"

def test_narrative_graph_checksum_and_validation():
    ng = NarrativeGraph(methodology=MethodologyType.ICT)
    node = NarrativeNode(
        node_id="n1",
        identity=NarrativeIdentity(
            methodology=MethodologyType.ICT,
            plugin_version="1.0",
            rule_version="1.0",
            graph_namespace="main",
            timeframe="4H",
            creation_sequence=1
        ),
        concept_type=NarrativeNodeType.POI,
        concept_name="Order Block POI",
        producer_plugin="ICTPlugin",
        producer_policy="ICTv1"
    )
    ng.add_node(node)
    
    # Checksum test
    csum = ng.checksum()
    assert isinstance(csum, str)
    assert len(csum) > 0
    
    # Validation test
    issues = ng.validate()
    assert len(issues["invalid_provenance"]) == 0
    assert len(issues["missing_type"]) == 0
    
    # Stats test
    stats = ng.statistics()
    assert stats["total_nodes"] == 1
    assert stats[f"count_{NarrativeNodeType.POI.value}"] == 1

from Backend.core.methodology.narrative_orchestrator import NarrativeOrchestrator

def test_narrative_orchestrator():
    orchestrator = NarrativeOrchestrator()
    plugin = StubICTPlugin()
    orchestrator.register_plugin(plugin)
    
    mtf = MultiTimeframeEvidenceGraph()
    mtf.add_timeframe("4H", EvidenceGraph())
    
    results = orchestrator.execute_all(mtf)
    assert MethodologyType.ICT.value in results
    assert len(results[MethodologyType.ICT.value].nodes) == 1

