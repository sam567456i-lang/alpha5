"""Composite Methodology Engine for aggregating multiple methodologies."""

from typing import List
from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation
from Backend.methodology.voting import AbstractVotingStrategy
from Backend.signals.primitive.context import SignalContext


class CompositeMethodology(AbstractMethodology):
    """
    Evaluates multiple inner methodologies and aggregates their signals 
    using an injected AbstractVotingStrategy.
    """
    
    def __init__(self, methodologies: List[AbstractMethodology], voting_strategy: AbstractVotingStrategy):
        if not methodologies:
            raise ValueError("CompositeMethodology requires at least one inner methodology.")
        if not voting_strategy:
            raise ValueError("CompositeMethodology requires a voting strategy.")
            
        self.methodologies = methodologies
        self.voting_strategy = voting_strategy

    @classmethod
    def get_name(cls) -> str:
        return "Composite"

    def evaluate(self, context: SignalContext) -> MethodologyEvaluation:
        """
        Evaluate all inner methodologies and aggregate the results.
        
        Args:
            context: The context of primitive signals.
            
        Returns:
            An aggregated MethodologyEvaluation based on the voting logic, or neutral if no consensus.
        """
        inner_signals = []
        for m in self.methodologies:
            sig = m.evaluate(context)
            inner_signals.append(sig)
            
        result = self.voting_strategy.vote(inner_signals)
        if result is None:
            # Neutral evaluation fallback
            return MethodologyEvaluation(
                methodology_id="Composite",
                timestamp=None,
                is_active=False,
                direction=0,
                confidence=0.0
            )
        return result
