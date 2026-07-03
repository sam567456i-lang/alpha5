"""Dependency Injection registry hook for the Methodology domain."""

import inspect
from Backend.foundation.dependency_injection_container import DependencyContainer
from Backend.methodology.engine import MethodologyEngine
from Backend.methodology.base import AbstractMethodology
import Backend.methodology as methodology_module

def register_methodologies(container: DependencyContainer) -> None:
    """
    Registers the Methodology domain components into the DI container.
    Auto-discovers and mounts all methodology plugins from the package namespace.
    """
    methodologies = []
    
    for name, obj in inspect.getmembers(methodology_module, inspect.isclass):
        if issubclass(obj, AbstractMethodology) and obj is not AbstractMethodology:
            try:
                methodologies.append(obj())
            except Exception as e:
                import logging
                logging.warning(f"Failed to load methodology plugin '{name}': {e}")
                
    container.register_factory("methodology_engine", lambda c: MethodologyEngine(methodologies=methodologies), singleton=True)
