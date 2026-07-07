from abc import ABC, abstractmethod
from typing import List, Dict, Any

from Backend.Platform10.contracts.dtos import MethodologyProfileDTO
from Backend.Platform11.contracts.dtos import CompositeMethodologyDTO

class SynthesisContext:
    """Mutable context passed through the synthesis pipeline."""
    def __init__(self, raw_methodologies: List[MethodologyProfileDTO]):
        self.raw_methodologies = raw_methodologies
        self.normalized_methodologies: Dict[str, Any] = {}
        self.compatibility_matrix: Dict[str, bool] = {}
        self.interaction_rules_applied: List[str] = []
        self.conflicts: Dict[str, str] = {}
        self.consensus_metrics: Dict[str, str] = {}
        self.evidence: Dict[str, Any] = {}
        self.explainability: str = ""
        self.numerical_intent: float = 0.0
        self.health_status: str = "Ready"
        self.missing_methodologies: List[str] = []
        self.active_methodologies: List[str] = []

class AbstractSynthesisEngine(ABC):
    """Base class for all Platform 11 synthesis engines."""
    
    @abstractmethod
    def execute(self, context: SynthesisContext) -> None:
        """Executes the specific phase of synthesis, mutating the context."""
        pass

    @property
    @abstractmethod
    def engine_name(self) -> str:
        pass
