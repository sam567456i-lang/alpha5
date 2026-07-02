"""Methodology Framework."""

from abc import ABC, abstractmethod
from Backend.signals.primitive.context import SignalContext
from .evaluation import MethodologyEvaluation


class AbstractMethodology(ABC):
    """
    Abstract template for a trading methodology (e.g., Trend Following, Mean Reversion).
    Evaluates semantic concepts and produces a MethodologyEvaluation.
    """

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        """Name of the methodology."""
        pass


    @abstractmethod
    def evaluate(self, context: 'SignalContext') -> MethodologyEvaluation:
        """
        Evaluates the current methodology context containing primitive signals.
        
        Args:
            context: The typed context containing all evaluated primitive signals.
            
        Returns:
            The evaluation result (direction, confidence, etc).
        """
        pass
