"""Concept Generation Framework."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
from .base import Concept


class AbstractConceptGenerator(ABC):
    """
    Base class for generating semantic concepts from feature values.
    """

    @classmethod
    @abstractmethod
    def get_id(cls) -> str:
        """Unique string identifier for this concept (e.g., 'MomentumExhaustion')."""
        pass

    @classmethod
    @abstractmethod
    def get_version(cls) -> str:
        """Version identifier."""
        pass

    @classmethod
    @abstractmethod
    def get_required_features(cls) -> List[str]:
        """List of feature names required to compute this concept."""
        return []

    @abstractmethod
    def evaluate(self, timestamp: datetime, feature_values: Dict[str, Any]) -> Concept:
        """
        Evaluates the concept based on feature inputs.
        
        Args:
            timestamp: The timestamp of the current event.
            feature_values: Dictionary of feature values.
            
        Returns:
            An immutable Concept object.
        """
        pass
