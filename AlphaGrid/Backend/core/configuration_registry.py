from typing import Dict, Any, List
from dataclasses import dataclass
from Backend.core.interfaces.core_interfaces import IConfigurationProvider

@dataclass(frozen=True)
class ConfigurationSnapshot:
    """Immutable snapshot of a configuration state."""
    policies: Dict[str, Any]
    features: Dict[str, Any]
    plugins: Dict[str, Any]
    capabilities: List[str]

class RuntimeConfiguration(IConfigurationProvider):
    """Read-only configuration available during execution."""
    def __init__(self, snapshot: ConfigurationSnapshot):
        self._snapshot = snapshot
        
    def get_config(self, key: str) -> Any:
        # Simplistic dot-notation or flat key lookup
        if key == "policies": return self._snapshot.policies
        if key == "features": return self._snapshot.features
        if key == "plugins": return self._snapshot.plugins
        if key == "capabilities": return self._snapshot.capabilities
        return None

class ConfigurationBuilder:
    """Builder pattern to construct a mutable configuration before freezing."""
    def __init__(self):
        self._policies: Dict[str, Any] = {}
        self._features: Dict[str, Any] = {}
        self._plugins: Dict[str, Any] = {}
        self._capabilities: List[str] = []
        
    def add_policy(self, name: str, config: Any):
        self._policies[name] = config
        return self
        
    def add_capability(self, name: str):
        self._capabilities.append(name)
        return self
        
    def build(self) -> ConfigurationSnapshot:
        return ConfigurationSnapshot(
            policies=dict(self._policies),
            features=dict(self._features),
            plugins=dict(self._plugins),
            capabilities=list(self._capabilities)
        )
