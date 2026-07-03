"""Dependency Injection registry hook for the Primitive Signals domain."""

import importlib
import pkgutil
import inspect
from Backend.foundation.dependency_injection_container import DependencyContainer
from Backend.signals.primitive.engine import PrimitiveSignalEngine
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator

def register_primitive_signals(container: DependencyContainer) -> None:
    """
    Registers the Primitive Signals domain components into the DI container.
    Auto-discovers and mounts all primitive signal generators.
    """
    generators = []
    
    # Auto-discover plugins in the generators package
    import Backend.signals.primitive.generators as generators_package
    package_name = generators_package.__name__
    package_path = generators_package.__path__
    
    for _, module_name, _ in pkgutil.iter_modules(package_path):
        try:
            module = importlib.import_module(f"{package_name}.{module_name}")
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, AbstractPrimitiveSignalGenerator) and obj is not AbstractPrimitiveSignalGenerator and obj.__module__ == module.__name__:
                    # Attempt to instantiate (same constraint as concepts - AD-004)
                    generators.append(obj())
        except Exception as e:
            import logging
            logging.warning(f"Failed to load primitive signal plugin '{module_name}': {e}")
                
    # PrimitiveSignalEngine does not use a Registry, it takes the list directly.
    container.register_factory("primitive_engine", lambda c: PrimitiveSignalEngine(generators=generators), singleton=True)
