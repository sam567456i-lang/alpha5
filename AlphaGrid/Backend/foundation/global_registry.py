import importlib
from typing import Dict, Any, Type, Optional
from .base_registry import BaseRegistry

class RegistryProvider:
    """Lazy loader for individual registries to optimize startup and allow dynamic plugin injection."""
    def __init__(self, module_path: str, class_name: str):
        self.module_path = module_path
        self.class_name = class_name
        self._instance: Optional[BaseRegistry] = None

    def get(self) -> BaseRegistry:
        if self._instance is None:
            module = importlib.import_module(self.module_path)
            registry_class = getattr(module, self.class_name)
            self._instance = registry_class()
        return self._instance

class GlobalRegistry:
    """
    The singular orchestration layer for all AlphaGrid registries.
    It does not store data directly; it strictly routes to specialized lazy-loaded providers.
    """
    def __init__(self):
        # We eagerly define the structure, but lazy-load the actual module instances.
        self._providers: Dict[str, RegistryProvider] = {
            "domain": RegistryProvider("Backend.core.domain_registry", "DomainRegistry"),
            "configuration": RegistryProvider("Backend.core.configuration_registry", "ConfigurationRegistry"),
            "artifact": RegistryProvider("Backend.core.artifact_registry", "ArtifactRegistry"),
            "market": RegistryProvider("Backend.core.market_registry", "MarketRegistry"),
            # New specialized registries will be added here as they are built in Phase 0.
        }

    def get_registry(self, name: str) -> BaseRegistry:
        if name not in self._providers:
            raise ValueError(f"[GlobalRegistry] Unknown registry requested: {name}")
        return self._providers[name].get()

    def verify_all(self) -> bool:
        """Forces instantiation of all registered providers and runs their integrity checks."""
        for name, provider in self._providers.items():
            registry = provider.get()
            if hasattr(registry, 'verify_integrity'):
                registry.verify_integrity()
        return True

    def export_global_manifest(self) -> Dict[str, Any]:
        """Collects the manifest from all loaded registries."""
        manifest = {"global_version": "1.0.0", "registries": {}}
        for name, provider in self._providers.items():
            # Only export loaded registries to avoid unnecessary instantiations
            if provider._instance is not None and hasattr(provider._instance, 'export_manifest'):
                manifest["registries"][name] = provider._instance.export_manifest()
        return manifest

# Singleton access
_global_registry_instance = GlobalRegistry()

def get_global_registry() -> GlobalRegistry:
    return _global_registry_instance
