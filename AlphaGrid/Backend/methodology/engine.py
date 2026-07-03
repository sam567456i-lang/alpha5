"""Methodology Engine.

Evaluates all registered methodologies to produce signals.
"""

from typing import List
import logging

from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation
from Backend.signals.primitive.context import SignalContext

logger = logging.getLogger(__name__)


class MethodologyEngine:
    """
    Executes a list of AbstractMethodology rules.
    It passes the SignalContext to each methodology and aggregates their evaluations.
    """

    ENGINE_METADATA = {
        "owner": "Methodology Domain",
        "version": "1.0.0",
        "consumes": "PrimitiveSignal",
        "produces": "MethodologyEvaluation",
        "registry": "methodology_registry",
        "contract_version": "v1",
        "downstream": "StrategyEngine"
    }

    def __init__(self, methodologies: List[AbstractMethodology]) -> None:
        """
        Initializes the MethodologyEngine.

        Args:
            methodologies: An ordered list of instantiated methodologies.
        """
        self.methodologies = methodologies

    def evaluate(self, context: SignalContext) -> List[MethodologyEvaluation]:
        """
        Evaluates all registered methodologies.

        Args:
            context: SignalContext containing PrimitiveSignals.

        Returns:
            A list of MethodologyEvaluation objects.
        """
        evaluations = []

        for methodology in self.methodologies:
            try:
                evaluation = methodology.evaluate(context)
                if evaluation.is_active:
                    evaluations.append(evaluation)
            except Exception as e:
                logger.error("Methodology '%s' evaluation failed: %s", methodology.get_name(), e)
                raise RuntimeError(f"Methodology '{methodology.get_name()}' evaluation failed") from e
                
        return evaluations
