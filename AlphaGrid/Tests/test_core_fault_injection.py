import pytest
import pandas as pd
from Backend.price_geometry.geometry_engine import GeometryEngineOrchestrator
from Backend.price_geometry.contracts import AbstractGeometryEngine
from Backend.price_geometry.registry import EngineRegistry

def test_circular_dependency_graceful_failure():
    """Validates the DAG gracefully rejects circular dependencies."""
    class AEngine(AbstractGeometryEngine):
        @property
        def engine_name(self) -> str: return "AEngine"
        @property
        def version(self) -> str: return "v1"
        def get_dependencies(self): return ["BEngine"]
        def process(self, data, context): return []
        def _asdict(self): return {"id": "AEngine"}
        
    class BEngine(AbstractGeometryEngine):
        @property
        def engine_name(self) -> str: return "BEngine"
        @property
        def version(self) -> str: return "v1"
        def get_dependencies(self): return ["AEngine"]
        def process(self, data, context): return []
        def _asdict(self): return {"id": "BEngine"}
        
    orchestrator = GeometryEngineOrchestrator()
    # Mock the registry for fault injection
    orchestrator.registry._items = {}
    orchestrator.registry.register("AEngine_v1", AEngine())
    orchestrator.registry.register("BEngine_v1", BEngine())
    
    with pytest.raises(ValueError, match="Cycle detected"):
        orchestrator._build_dag()

def test_missing_context_injection():
    """Validates graceful failure when context lacks geometry_cache."""
    orchestrator = GeometryEngineOrchestrator()
    
    class BadContext:
        pass
        
    with pytest.raises(ValueError, match="requires context.geometry_cache"):
        orchestrator.process_all(pd.DataFrame(), BadContext())
