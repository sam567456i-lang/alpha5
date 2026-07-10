from abc import ABC, abstractmethod
from typing import Any, List

class BaseEngine(ABC):
    """
    Template Method enforcing a strict execution lifecycle for all analytical engines.
    """
    def execute(self, inputs: Any) -> List[Any]:
        self.initialize()
        self.validate_inputs(inputs)
        features = self.request_features()
        raw_evidence = self.execute_rules(inputs, features)
        self.validate_evidence(raw_evidence)
        self.publish(raw_evidence)
        self.cleanup()
        return raw_evidence

    @abstractmethod
    def initialize(self): pass

    @abstractmethod
    def validate_inputs(self, inputs: Any): pass

    @abstractmethod
    def request_features(self) -> Any: pass

    @abstractmethod
    def execute_rules(self, inputs: Any, features: Any) -> List[Any]: pass

    def validate_evidence(self, evidence: List[Any]):
        """Ensure evidence is correctly classified and immutable."""
        pass

    def publish(self, evidence: List[Any]):
        """Publish to the Evidence Graph via SDK."""
        pass

    def cleanup(self):
        """Release temporary resources."""
        pass
