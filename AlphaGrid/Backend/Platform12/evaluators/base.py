from abc import ABC, abstractmethod
from typing import List, Dict, Any
from Backend.Platform12.contracts.dtos import OpportunityDetectionDTO

class AbstractOpportunityEvaluator(ABC):
    @property
    @abstractmethod
    def evaluator_id(self) -> str:
        pass
        
    @property
    @abstractmethod
    def required_methodologies(self) -> List[str]:
        pass
        
    @property
    @abstractmethod
    def supported_markets(self) -> List[str]:
        pass
        
    @property
    @abstractmethod
    def supported_timeframes(self) -> List[str]:
        pass
        
    @property
    @abstractmethod
    def produces_opportunity_types(self) -> List[str]:
        pass
        
    @abstractmethod
    def evaluate(self, composite_context: Any, profile: Dict[str, Any]) -> List[OpportunityDetectionDTO]:
        """Evaluates the context and returns opportunities if detected."""
        pass
