"""Methodology Framework."""

from abc import ABC, abstractmethod
from typing import Dict, List
from Backend.concepts.base import Concept
from .signals import Signal


class AbstractMethodology(ABC):
    """
    Abstract template for a trading methodology (e.g., Trend Following, Mean Reversion).
    Evaluates semantic concepts and produces a rich Signal.
    """

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        """Name of the methodology."""
        pass

    @classmethod
    @abstractmethod
    def get_required_concepts(cls) -> List[str]:
        """List of concept IDs required by this methodology."""
        return []

    @abstractmethod
    def evaluate(self, concepts: Dict[str, Concept]) -> Signal:
        """
        Evaluates the methodology logic given the current concepts.
        
        Args:
            concepts: Dictionary mapping concept IDs to immutable Concept objects.
            
        Returns:
            A rich Signal object.
        """
        pass
