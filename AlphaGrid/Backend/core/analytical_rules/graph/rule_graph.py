import networkx as nx
from typing import List, Dict, Set, Any

class RuleDependencyGraph:
    """
    Represents the acyclic directed graph of analytical rules.
    Validates DAG, resolves dependencies, and computes topological order.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def add_rule(self, rule_id: str, dependencies: List[str]):
        """Adds a rule and its dependencies to the graph."""
        self.graph.add_node(rule_id)
        for dep in dependencies:
            self.graph.add_edge(dep, rule_id)
            
    def validate_dag(self) -> bool:
        """Checks for circular dependencies."""
        return nx.is_directed_acyclic_graph(self.graph)
        
    def get_cycles(self) -> List[List[str]]:
        """Returns a list of cycles if they exist."""
        try:
            return list(nx.simple_cycles(self.graph))
        except nx.NetworkXNoCycle:
            return []

    def get_topological_order(self) -> List[str]:
        """Returns the execution order based on dependencies."""
        if not self.validate_dag():
            raise ValueError(f"Graph contains cycles: {self.get_cycles()}")
        return list(nx.topological_sort(self.graph))

    def get_unreachable_nodes(self, starting_nodes: List[str]) -> Set[str]:
        """Detects nodes that cannot be reached from the given starting nodes."""
        reachable = set()
        for start in starting_nodes:
            if start in self.graph:
                reachable.update(nx.descendants(self.graph, start))
                reachable.add(start)
        return set(self.graph.nodes()) - reachable

    def get_dependencies(self, rule_id: str) -> List[str]:
        """Returns immediate dependencies for a given rule."""
        if rule_id not in self.graph:
            return []
        return list(self.graph.predecessors(rule_id))

class RuleGraphBuilder:
    """
    Constructs the RuleDependencyGraph from a set of rules.
    """
    def build(self, rules: List[Any]) -> RuleDependencyGraph:
        graph = RuleDependencyGraph()
        for rule in rules:
            # Assuming rule objects have a get_capabilities() returning id and get_dependencies()
            # For Tier0 we might just identify by their producer id like "RULE-T0-001"
            # Here we expect rules to be instantiated SDK implementations
            cap = rule.get_capabilities()
            rule_id = cap.get("capability_id") # e.g. CAP-T0-001 or we use the rule ID directly.
            # Using rule class name or defined ID
            deps = rule.get_dependencies()
            graph.add_rule(rule.__class__.__name__, deps)
        return graph
