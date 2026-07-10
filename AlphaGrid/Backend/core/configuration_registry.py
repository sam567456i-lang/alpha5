from typing import Dict, Any, List
from dataclasses import dataclass
from Backend.foundation.base_registry import BaseRegistry

@dataclass(frozen=True)
class ConfigurationSnapshot:
    """Immutable snapshot of a configuration state."""
    policies: Dict[str, Any]
    features: Dict[str, Any]
    plugins: Dict[str, Any]
    capabilities: List[str]

class ConfigurationRegistry(BaseRegistry[ConfigurationSnapshot]):
    """
    Active Configuration Registry.
    Responsible for active configurations, version lookup, profile lookup, and runtime access.
    """
    def __init__(self):
        super().__init__("ConfigurationRegistry")
        self._active_profile: str = "default"
        
    def set_active_profile(self, profile_name: str):
        if not self.get(profile_name):
            raise ValueError(f"Profile {profile_name} is not registered in ConfigurationRegistry.")
        self._active_profile = profile_name

    def get_active(self) -> ConfigurationSnapshot:
        active = self.get(self._active_profile)
        if not active:
            raise RuntimeError("No active configuration profile found.")
        return active

    def resolve_dependency_config(self, dependency_name: str) -> Any:
        """Looks up the configuration specifically tailored for a requested dependency."""
        active = self.get_active()
        return active.plugins.get(dependency_name, {})
