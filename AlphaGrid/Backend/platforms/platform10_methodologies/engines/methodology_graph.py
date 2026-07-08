from typing import Dict, List, Set

class MethodologyGraph:
    """
    Lightweight, pure Python DAG for mapping relationships between methodologies/concepts.
    Absolutely no dependencies on NetworkX.
    Does NOT contain methodology-specific logic (e.g. ICT, SMC). It only understands relationships:
    - supports
    - requires
    - invalidates
    - enhances
    - conflicts
    """
    def __init__(self):
        self.nodes: Set[str] = set()
        self.edges: Dict[str, Dict[str, List[str]]] = {} # {node_a: {node_b: [relationship_types]}}

    def add_node(self, node_id: str):
        self.nodes.add(node_id)
        if node_id not in self.edges:
            self.edges[node_id] = {}

    def add_edge(self, source: str, target: str, relationship: str):
        self.add_node(source)
        self.add_node(target)
        if target not in self.edges[source]:
            self.edges[source][target] = []
        if relationship not in self.edges[source][target]:
            self.edges[source][target].append(relationship)

    def get_dependencies(self, node_id: str, relationship: str = "requires") -> List[str]:
        deps = []
        if node_id in self.edges:
            for target, rels in self.edges[node_id].items():
                if relationship in rels:
                    deps.append(target)
        return deps
