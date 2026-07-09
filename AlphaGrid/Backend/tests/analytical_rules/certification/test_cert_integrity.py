import pytest
from Backend.core.analytical_rules.capabilities.evidence_graph import EvidenceGraph

def get_populated_graph() -> EvidenceGraph:
    return EvidenceGraph()

def test_cert_graph_integrity():
    """
    Suite 5: Graph Integrity Validation
    Ensures the graph adheres to strict graph-theory rules (no orphans, DAG violations, duplicates).
    """
    graph = get_populated_graph()
    
    validation_results = graph.validate()
    
    assert len(validation_results["orphans"]) == 0, f"Found orphan nodes: {validation_results['orphans']}"
    assert len(validation_results["dangling_references"]) == 0, f"Found dangling references: {validation_results['dangling_references']}"
    assert len(validation_results["lineage_failures"]) == 0, f"Found lineage failures: {validation_results['lineage_failures']}"
