"""Dependency Injection registry hook for the Feature domain."""

import importlib
import pkgutil
import inspect
from Backend.foundation.dependency_injection_container import DependencyContainer
from Backend.features.registry import FeatureRegistry
from Backend.features.engine import FeatureEngine
from Backend.features.base import AbstractFeature

def register_features(container: DependencyContainer) -> None:
    """
    Registers the Feature domain components into the DI container.
    Auto-discovers and mounts all feature plugins.
    """
    registry = FeatureRegistry()
    
    # Auto-discover plugins
    import Backend.features as features_package
    package_name = features_package.__name__
    package_path = features_package.__path__
    
    for _, module_name, _ in pkgutil.iter_modules(package_path):
        if module_name not in ["base", "registry", "engine", "registry_hook", "protocols", "cache"]:
            try:
                module = importlib.import_module(f"{package_name}.{module_name}")
                # Find all classes in the module that inherit from AbstractFeature
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, AbstractFeature) and obj is not AbstractFeature and obj.__module__ == module.__name__:
                        registry.register(obj)
            except Exception as e:
                import logging
                logging.warning(f"Failed to load feature plugin '{module_name}': {e}")
                
    # Mount into DI container as singletons
    container.register_factory("feature_registry", lambda c: registry, singleton=True)
    container.register_factory("feature_engine", lambda c: FeatureEngine(registry=registry), singleton=True)
