"""Geometry Factory for auto-discovering engines."""

import importlib
import pkgutil
from typing import Dict, Type
from Backend.price_geometry.contracts import AbstractGeometryEngine
from Backend.price_geometry.registry import EngineRegistry

class GeometryFactory:
    """
    Auto-discovers and constructs Geometry Engines.
    Uses the EngineRegistry to manage instances.
    """
    def __init__(self, registry: EngineRegistry):
        self._registry = registry
        self._engine_classes: Dict[str, Type[AbstractGeometryEngine]] = {}
        
    def discover_engines(self, package_name: str = "Backend.price_geometry") -> None:
        """Scan package for classes implementing AbstractGeometryEngine."""
        package = importlib.import_module(package_name)
        
        for _, module_name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            try:
                module = importlib.import_module(module_name)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, AbstractGeometryEngine) and attr is not AbstractGeometryEngine:
                        engine_name = attr.__name__
                        self._engine_classes[engine_name] = attr
            except ImportError:
                continue
                
    def create_engine(self, engine_name: str, **kwargs) -> AbstractGeometryEngine:
        """Construct an engine by name and register it."""
        if engine_name not in self._engine_classes:
            raise ValueError(f"Geometry engine '{engine_name}' not found. Run discover_engines() first.")
            
        engine_class = self._engine_classes[engine_name]
        engine_instance = engine_class(**kwargs)
        self._registry.register_engine(engine_instance)
        return engine_instance
