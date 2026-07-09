import pytest
import gc
import weakref
from Backend.core.analytical_rules.capabilities.evidence_graph import EvidenceGraph

def build_graph() -> EvidenceGraph:
    graph = EvidenceGraph()
    graph.structure_nodes["test_node"] = "test_state"
    return graph

def test_cert_memory_leak():
    """
    Suite 9: Memory Leak Certification
    Runs 100 loops of Build -> Destroy -> GC to assert stable memory 
    and zero retained graph objects. Catches subtle lifecycle reference bugs.
    """
    refs = []
    
    for _ in range(100):
        graph = build_graph()
        refs.append(weakref.ref(graph))
        del graph
        
    gc.collect()
    
    retained_count = sum(1 for ref in refs if ref() is not None)
    
    assert retained_count == 0, f"Memory leak detected: {retained_count} EvidenceGraph objects retained after GC."
