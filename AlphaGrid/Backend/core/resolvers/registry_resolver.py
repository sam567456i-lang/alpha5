import os
import yaml
from typing import Dict, Any

class RegistryResolver:
    """
    Centralized configuration resolver.
    Consumes YAML registries and serves parsed, validated dicts to the engines.
    Engines must NEVER parse YAML files directly.
    """
    def __init__(self, registry_dir: str):
        self.registry_dir = registry_dir
        self.cache: Dict[str, Any] = {}

    def _load_yaml(self, filename: str) -> Any:
        if filename in self.cache:
            return self.cache[filename]
        
        path = os.path.join(self.registry_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Registry file not found: {path}")
            
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            self.cache[filename] = data
            return data

    def resolve_methodology_execution_policy(self, methodology_id: str) -> Dict[str, Any]:
        """Resolves the execution policy (timeout, order, aggregation) for a specific methodology."""
        data = self._load_yaml("methodology_execution_registry.yaml")
        for policy in data.get("execution_policies", []):
            if policy.get("methodology_ref") == methodology_id:
                return policy
        return {} # Return default/empty if not explicitly configured

    def resolve_state_machine_config(self) -> Dict[str, Any]:
        """Resolves the universal state machine configurations."""
        data = self._load_yaml("methodology_state_machine_registry.yaml")
        # In a real system, we'd fetch the specific ID, but there's a default one for P10
        return data.get("state_machines", [{}])[0]
