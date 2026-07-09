from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from Backend.core.interfaces.core_interfaces import IFeatureStore
from Backend.core.analytical_rules.dto.feature_evidence_dto import FeatureEvidenceDTO

@dataclass
class FeatureIdentity:
    name: str
    version: str

@dataclass
class FeatureDefinition:
    identity: FeatureIdentity
    dependencies: List[str] # List of FeatureIdentity names
    policy_hash: str

class FeatureDependencyGraph:
    def __init__(self):
        self.dependencies: Dict[str, List[str]] = {} # feature -> relies_on
        self.dependents: Dict[str, List[str]] = {}   # feature -> relied_by
        
    def add_feature(self, definition: FeatureDefinition):
        name = definition.identity.name
        if name not in self.dependencies:
            self.dependencies[name] = []
        if name not in self.dependents:
            self.dependents[name] = []
            
        for dep in definition.dependencies:
            self.dependencies[name].append(dep)
            if dep not in self.dependents:
                self.dependents[dep] = []
            self.dependents[dep].append(name)

class InvalidationEngine:
    def __init__(self, graph: FeatureDependencyGraph, store: IFeatureStore):
        self.graph = graph
        self.store = store
        
    def invalidate(self, trigger_feature: str):
        # Invalidate this feature
        self.store.invalidate(trigger_feature)
        # Cascade down the DAG
        dependents = self.graph.dependents.get(trigger_feature, [])
        for dep in dependents:
            self.invalidate(dep)

class FeatureStore(IFeatureStore):
    """Tiered Feature Store (L1 InMemory, L2 Placeholder)"""
    def __init__(self):
        self.l1_cache: Dict[str, Any] = {}
        
    def get_feature(self, feature_id: str) -> Optional[Any]:
        return self.l1_cache.get(feature_id)
        
    def set_feature(self, feature_id: str, data: Any, dependencies: List[str]):
        self.l1_cache[feature_id] = data
        
    def invalidate(self, feature_id: str):
        if feature_id in self.l1_cache:
            del self.l1_cache[feature_id]
