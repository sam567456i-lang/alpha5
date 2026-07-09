import yaml
import os
from typing import Dict, List, Any
from Backend.core.methodology.narrative_graph import NarrativeGraph
from Backend.core.methodology.narrative_types import NarrativeNodeType

class NarrativeDependencyValidator:
    """
    Validates a NarrativeGraph against the governance rules defined in narrative_registry.yaml.
    Enforces that nodes have their required supporting narratives before they are permitted.
    """
    def __init__(self, registry_path: str = None):
        if registry_path is None:
            # Default to the registry in the same directory
            registry_path = os.path.join(os.path.dirname(__file__), "narrative_registry.yaml")
        
        with open(registry_path, "r") as f:
            self.registry_data = yaml.safe_load(f)
            
        self.rules: Dict[str, Dict[str, Any]] = {}
        for node_def in self.registry_data.get("nodes", []):
            self.rules[node_def["type"]] = node_def

    def validate(self, graph: NarrativeGraph) -> Dict[str, List[str]]:
        """
        Validates the graph's dependencies.
        Returns a dictionary of violations. If empty, the graph is valid.
        """
        violations = {"missing_required_dependencies": [], "unauthorized_methodology": []}
        
        for node_id, node in graph.nodes.items():
            node_type_str = node.concept_type.value
            
            # Check if this node type is governed by the registry
            if node_type_str not in self.rules:
                # If it's a custom node or missing from registry, we might skip or flag
                continue
                
            rule = self.rules[node_type_str]
            
            # 1. Check methodology authorization
            node_methodology = node.identity.methodology.value if node.identity else None
            if node_methodology not in rule.get("methodologies", []):
                violations["unauthorized_methodology"].append(f"{node_id} ({node_type_str}) by {node_methodology}")
                
            # 2. Check required dependencies
            required_deps = rule.get("required", [])
            if required_deps:
                # Find all narrative types that this node supports
                supported_types = set()
                for supp_id in node.supporting_narrative_ids:
                    supp_node = graph.find(supp_id)
                    if supp_node:
                        supported_types.add(supp_node.concept_type.value)
                        
                for req in required_deps:
                    if req not in supported_types:
                        violations["missing_required_dependencies"].append(f"{node_id} ({node_type_str}) requires {req}")
                        
        return violations
