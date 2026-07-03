from Backend.foundation.base_registry import BaseRegistry
from Backend.price_geometry.contracts import AbstractGeometryEngine

class EngineRegistry(BaseRegistry[AbstractGeometryEngine]):
    """
    Registry for Geometry Engines.
    Ensures algorithms are explicitly versioned (e.g., SwingEngineV1, SwingEngineV2).
    """
    def __init__(self):
        super().__init__("GeometryEngineRegistry", version="1.0.0")
        
    def register_engine(self, engine: AbstractGeometryEngine) -> None:
        key = f"{engine.engine_name}_{engine.version}"
        self.register(key, engine)
