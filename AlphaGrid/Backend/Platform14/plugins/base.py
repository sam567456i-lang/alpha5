from abc import ABC, abstractmethod
from typing import Dict, Any
from Backend.Platform14.contracts.dtos import RecommendationDTO

class AbstractPlugin(ABC):
    @property
    @abstractmethod
    def plugin_id(self) -> str:
        pass

class AbstractGeneratorPlugin(AbstractPlugin):
    @abstractmethod
    def generate(self, dto: RecommendationDTO, policy: Dict[str, Any]) -> None:
        """Calculates and sets fields like entry, stop, or targets."""
        pass

class AbstractAnalyzerPlugin(AbstractPlugin):
    @abstractmethod
    def analyze(self, dto: RecommendationDTO, policy: Dict[str, Any]) -> None:
        """Calculates derived metrics like R:R or trade structure."""
        pass

class AbstractBuilderPlugin(AbstractPlugin):
    @abstractmethod
    def build(self, dto: RecommendationDTO, policy: Dict[str, Any]) -> None:
        """Finalizes the recommendation, adding notes and confidence."""
        pass
