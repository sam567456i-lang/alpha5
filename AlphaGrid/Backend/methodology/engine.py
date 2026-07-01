"""Methodology Engine.

Evaluates all registered methodologies to produce signals.
"""

from typing import Dict, List
import logging

from Backend.concepts.base import Concept
from Backend.methodology.base import AbstractMethodology
from Backend.methodology.signals import Signal

logger = logging.getLogger(__name__)


class MethodologyEngine:
    """
    Evaluates multiple methodologies given the current concept state.
    """

    def __init__(self, methodologies: List[AbstractMethodology]) -> None:
        self._methodologies = methodologies

    def evaluate(self, concepts: Dict[str, Concept]) -> List[Signal]:
        """
        Evaluates all registered methodologies.

        Args:
            concepts: Dictionary of current concepts mapped by ID.

        Returns:
            A list of actionable Signals (excludes WAIT signals).
        """
        signals = []
        for methodology in self._methodologies:
            # Check if all required concepts exist and have >0 confidence
            required = methodology.get_required_concepts()
            can_evaluate = all(
                cid in concepts and concepts[cid].confidence > 0.0
                for cid in required
            )
            
            if not can_evaluate:
                continue
                
            try:
                signal = methodology.evaluate(concepts)
                if signal.direction != "WAIT":
                    signals.append(signal)
            except Exception as e:
                logger.error("Methodology '%s' evaluation failed: %s", methodology.get_name(), e)
                raise RuntimeError(f"Methodology '{methodology.get_name()}' evaluation failed") from e
                
        return signals
