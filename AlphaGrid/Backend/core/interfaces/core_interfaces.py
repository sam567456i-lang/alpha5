from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class IFeatureStore(ABC):
    @abstractmethod
    def get_feature(self, feature_id: str) -> Optional[Any]:
        pass

    @abstractmethod
    def set_feature(self, feature_id: str, data: Any, dependencies: List[str]):
        pass
        
    @abstractmethod
    def invalidate(self, feature_id: str):
        pass

class IArtifactRegistry(ABC):
    @abstractmethod
    def register_artifact(self, artifact_type: str, data: Any, provenance: Dict[str, Any]) -> str:
        pass
        
    @abstractmethod
    def get_artifact(self, artifact_id: str) -> Optional[Any]:
        pass

class ITelemetry(ABC):
    @abstractmethod
    def emit_metric(self, name: str, value: float, tags: Dict[str, str]):
        pass
        
    @abstractmethod
    def emit_health(self, component: str, status: str, details: Dict[str, Any]):
        pass

class ISnapshotStore(ABC):
    @abstractmethod
    def save_snapshot(self, snapshot_id: str, data: bytes, level: str):
        pass
        
    @abstractmethod
    def load_snapshot(self, snapshot_id: str) -> Optional[bytes]:
        pass

class IConfigurationProvider(ABC):
    @abstractmethod
    def get_config(self, key: str) -> Any:
        pass

class IResourceManager(ABC):
    @abstractmethod
    def allocate(self, component: str, memory_mb: int, cpu_shares: int) -> bool:
        pass
        
    @abstractmethod
    def release(self, component: str):
        pass

class ICapabilityScheduler(ABC):
    @abstractmethod
    def schedule(self, execution_plan: Any):
        pass
