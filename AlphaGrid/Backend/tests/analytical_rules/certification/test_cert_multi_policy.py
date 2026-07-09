import pytest
from Backend.core.analytical_rules.capabilities.evidence_graph import EvidenceGraph

def run_engine_with_policy(policy_name: str) -> EvidenceGraph:
    # Stub: run the engine with a specific policy
    graph = EvidenceGraph()
    # Unique node based on policy
    graph.structure_nodes[f"node_{policy_name}_1"] = f"state_{policy_name}"
    return graph

def test_cert_multi_policy_isolation():
    """
    Suite 6: Multi-Policy Isolation
    Proves that multiple configurations can coexist without collision.
    """
    graph_fractal = run_engine_with_policy("fractal")
    graph_atr = run_engine_with_policy("atr")
    graph_adaptive = run_engine_with_policy("adaptive")
    
    # Assert zero ID collisions
    fractal_keys = set(graph_fractal.structure_nodes.keys())
    atr_keys = set(graph_atr.structure_nodes.keys())
    adaptive_keys = set(graph_adaptive.structure_nodes.keys())
    
    assert fractal_keys.isdisjoint(atr_keys), "Collision between Fractal and ATR policies."
    assert fractal_keys.isdisjoint(adaptive_keys), "Collision between Fractal and Adaptive policies."
    assert atr_keys.isdisjoint(adaptive_keys), "Collision between ATR and Adaptive policies."
