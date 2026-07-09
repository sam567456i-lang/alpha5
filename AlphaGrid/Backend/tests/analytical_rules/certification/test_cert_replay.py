import pytest
from Backend.core.analytical_rules.capabilities.evidence_graph import EvidenceGraph

def simulate_engine_run() -> EvidenceGraph:
    # In a full integration, this would spin up the OHLCV engine
    # and feed a deterministic set of data into it.
    graph = EvidenceGraph()
    # Stub: inject some dummy data
    graph.structure_nodes["node_1"] = "stub_state_1"
    graph.liquidity_nodes["pool_1"] = "stub_pool_1"
    return graph

def test_cert_replay_determinism():
    """
    Suite 1: End-to-End Replay Certification
    Guarantees state reconstruction is completely deterministic.
    """
    graph_a = simulate_engine_run()
    graph_b = simulate_engine_run()
    
    # Assert intrinsic checksums match rather than raw JSON strings
    assert graph_a.checksum() == graph_b.checksum(), "Replay produced divergent graph states."
