"""Abstract interface for AlphaGrid Research Features (Phase 8)."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from Shared.models.market import MarketSnapshot


class AbstractFeature(ABC):
    """
    Base class for all research features.
    Guarantees consistent metadata, dependency declaration, and determinism.
    """

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        """Unique string identifier for this feature (e.g., 'EMA_20')."""
        pass

    @classmethod
    @abstractmethod
    def get_version(cls) -> str:
        """Version identifier to freeze feature logic (e.g., 'v1')."""
        pass

    @classmethod
    def get_dependencies(cls) -> List[str]:
        """
        List of feature names this feature depends on.
        The registry uses this to build a topological execution DAG.
        """
        return []

    @classmethod
    def warmup_period(cls) -> int:
        """
        Number of historical bars required before the feature emits valid data.
        The Feature Engine will handle None outputs during this period.
        """
        return 0

    @abstractmethod
    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Any:
        """
        Computes the feature value deterministically.
        
        Args:
            snapshot: The current market event.
            dependency_values: Dictionary of pre-computed feature dependencies.
            
        Returns:
            The computed feature value (float, dict, etc.) or None if warming up.
        """
        pass
