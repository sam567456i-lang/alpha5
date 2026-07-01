"""Decision Provider Interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List
from Backend.methodology.signals import Signal


@dataclass(frozen=True)
class Decision:
    """
    The final decision produced by a Decision Provider.
    This is passed back to the Strategy.
    """
    direction: str  # e.g., 'LONG', 'SHORT', 'WAIT'
    confidence: float
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class AbstractDecisionProvider(ABC):
    """
    Base interface for all Decision Providers (Rule-based or ML-based).
    Strategies must rely on this interface, remaining completely unaware
    of whether rules or neural networks are generating the decision.
    """

    @abstractmethod
    def evaluate(self, signals: List[Signal], context: Dict[str, Any]) -> Decision:
        """
        Evaluates the current market context and signals to produce a Decision.
        
        Args:
            signals: List of rich Signal objects from Methodology Evaluation.
            context: Additional market context or feature states if required.
            
        Returns:
            A final Decision object.
        """
        pass
