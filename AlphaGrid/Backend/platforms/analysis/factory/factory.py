from typing import Type, Dict
from Backend.platforms.analysis.core.dto import AnalysisContext, AnalysisResult
from Backend.platforms.analysis.registry.loader import RegistryLoader

class BaseAnalysis:
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        raise NotImplementedError()

class AnalysisFactory:
    def __init__(self, loader: RegistryLoader):
        self.loader = loader
        self._implementations: Dict[str, Type[BaseAnalysis]] = {}
        
    def register(self, capability_id: str, impl: Type[BaseAnalysis]):
        # Ensure it exists in registry first
        self.loader.get_metadata(capability_id) 
        self._implementations[capability_id] = impl
        
    def create(self, capability_id: str) -> BaseAnalysis:
        impl = self._implementations.get(capability_id)
        if not impl:
            raise ValueError(f"No implementation registered for {capability_id}")
        return impl()
