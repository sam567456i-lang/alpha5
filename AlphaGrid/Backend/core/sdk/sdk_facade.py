from abc import ABC, abstractmethod
from typing import Any, List

class IEvidenceSDK(ABC):
    @abstractmethod
    def query(self, query_params: Any) -> List[Any]: pass
    
    @abstractmethod
    def subscribe(self, event_type: str, callback: Any): pass

class IFeatureSDK(ABC):
    @abstractmethod
    def get_feature(self, feature_id: str) -> Any: pass

class ICapabilitySDK(ABC):
    @abstractmethod
    def request_capability(self, capability_name: str, params: Any) -> Any: pass

class IReplaySDK(ABC):
    @abstractmethod
    def start_replay(self, start_time: Any, end_time: Any, speed: float): pass
