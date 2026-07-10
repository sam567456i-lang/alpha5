from typing import List, Dict
from Backend.core.methodologies.core_models import MethodologyInstance, MethodologyContext
from Backend.core.methodologies.evidence import MethodologyClaim

class CompositionNode:
    def __init__(self, instance: MethodologyInstance, dependencies: List['CompositionNode'] = None):
        self.instance = instance
        self.dependencies = dependencies or []
        self._cached_claims: List[MethodologyClaim] = []
        self._is_evaluated = False

    def evaluate_node(self, context: MethodologyContext) -> List[MethodologyClaim]:
        if self._is_evaluated:
            return self._cached_claims
            
        # Ensure dependencies are evaluated first
        for dep in self.dependencies:
            dep.evaluate_node(context)
            
        # In a real implementation, the node would inject dependency claims into a local 
        # sub-context for the current instance. For now, we just evaluate.
        self._cached_claims = self.instance.evaluate(context)
        self._is_evaluated = True
        return self._cached_claims

class CompositionGraph:
    """A DAG representing methodology dependencies for composite execution."""
    def __init__(self):
        self.nodes: Dict[str, CompositionNode] = {}
        
    def add_node(self, node_id: str, instance: MethodologyInstance, deps: List[str]):
        # Prevent cycles during registration
        self._detect_cycles(node_id, deps)
        
        dependency_nodes = [self.nodes[d] for d in deps]
        self.nodes[node_id] = CompositionNode(instance, dependency_nodes)
        
    def _detect_cycles(self, node_id: str, deps: List[str]):
        # Simple cycle detection (mocked for brevity)
        if node_id in deps:
            raise ValueError(f"Cycle detected in CompositionGraph for node {node_id}")

    def execute_graph(self, context: MethodologyContext) -> Dict[str, List[MethodologyClaim]]:
        results = {}
        for node_id, node in self.nodes.items():
            results[node_id] = node.evaluate_node(context)
        return results
