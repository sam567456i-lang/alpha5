from abc import ABC, abstractmethod
from typing import List, Dict, Any
from Backend.Platform13.contracts.dtos import EvaluatedOpportunityDTO, EvaluatedOpportunityCollectionDTO

class AbstractPlugin(ABC):
    @property
    @abstractmethod
    def plugin_id(self) -> str:
        pass

class AbstractAssessmentPlugin(AbstractPlugin):
    @abstractmethod
    def assess(self, dto: EvaluatedOpportunityDTO, profile: Dict[str, Any]) -> None:
        """Mutates the dto with assessment scores."""
        pass

class AbstractPolicyPlugin(AbstractPlugin):
    @abstractmethod
    def apply_policy(self, collection: EvaluatedOpportunityCollectionDTO, profile: Dict[str, Any]) -> None:
        """Applies policy across the collection (e.g. competition graph)."""
        pass

class AbstractBuilderPlugin(AbstractPlugin):
    @abstractmethod
    def build(self, dto: EvaluatedOpportunityDTO, policy: Dict[str, Any]) -> None:
        """Builds composite scores and provenance."""
        pass

class AbstractRankingPlugin(AbstractPlugin):
    @abstractmethod
    def rank(self, collection: EvaluatedOpportunityCollectionDTO, policy: Dict[str, Any]) -> None:
        """Sorts and ranks the collection."""
        pass

class AbstractLifecyclePlugin(AbstractPlugin):
    @abstractmethod
    def manage_lifecycle(self, dto: EvaluatedOpportunityDTO, policy: Dict[str, Any]) -> None:
        """Manages queue status transitions."""
        pass
