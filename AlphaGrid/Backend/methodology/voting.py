"""Voting strategies for Methodology aggregation."""

from abc import ABC, abstractmethod
from typing import Sequence, Optional, List
from Backend.methodology.evaluation import MethodologyEvaluation
from datetime import datetime, timezone

class AbstractVotingStrategy(ABC):
    """
    Defines the contract for aggregating signals from multiple methodologies.
    Extensible to support Majority, Unanimous, Weighted, Bayesian, etc.
    """
    
    @abstractmethod
    def vote(self, evaluations: Sequence[Optional[MethodologyEvaluation]]) -> Optional[MethodologyEvaluation]:
        """
        Aggregates a list of methodology evaluations into a single output evaluation.
        
        Args:
            evaluations: The evaluations emitted by the inner methodologies.
            
        Returns:
            The aggregated MethodologyEvaluation, or None if no consensus is reached.
        """
        pass


class UnanimousVoting(AbstractVotingStrategy):
    """All inner methodologies must agree on the direction."""
    
    def vote(self, evaluations: Sequence[Optional[MethodologyEvaluation]]) -> Optional[MethodologyEvaluation]:
        valid_evals = [e for e in evaluations if e is not None and e.is_active]
        if not valid_evals or len(valid_evals) != len(evaluations):
            return None
            
        directions = {e.direction for e in valid_evals}
        if len(directions) == 1:
            # Everyone agrees
            direction = directions.pop()
            avg_conf = sum(e.confidence for e in valid_evals) / len(valid_evals)
            
            # Combine concepts
            concepts = {}
            for e in valid_evals:
                concepts.update(e.supporting_concepts)
                
            return MethodologyEvaluation(
                methodology_id="Composite-Unanimous",
                timestamp=valid_evals[0].timestamp if valid_evals[0].timestamp else datetime.now(timezone.utc),
                is_active=True,
                direction=direction,
                confidence=avg_conf,
                supporting_concepts=concepts
            )
            
        return None


class MajorityVoting(AbstractVotingStrategy):
    """Over 50% of inner methodologies must agree on the direction."""
    
    def vote(self, evaluations: Sequence[Optional[MethodologyEvaluation]]) -> Optional[MethodologyEvaluation]:
        valid_evals = [e for e in evaluations if e is not None and e.is_active]
        if not valid_evals:
            return None
            
        longs = [e for e in valid_evals if e.direction == 1]
        shorts = [e for e in valid_evals if e.direction == -1]
        flats = [e for e in valid_evals if e.direction == 0]
        
        required_majority = len(evaluations) // 2 + 1
        
        # Helper to construct result
        def _build_eval(subset: List[MethodologyEvaluation], direction: int) -> MethodologyEvaluation:
            avg_conf = sum(e.confidence for e in subset) / len(subset)
            concepts = {}
            for e in subset:
                concepts.update(e.supporting_concepts)
            return MethodologyEvaluation(
                methodology_id="Composite-Majority",
                timestamp=subset[0].timestamp if subset[0].timestamp else datetime.now(timezone.utc),
                is_active=True,
                direction=direction,
                confidence=avg_conf,
                supporting_concepts=concepts
            )
            
        if len(longs) >= required_majority:
            return _build_eval(longs, 1)
            
        if len(shorts) >= required_majority:
            return _build_eval(shorts, -1)
            
        if len(flats) >= required_majority:
            return _build_eval(flats, 0)
            
        return None


class AnyVoting(AbstractVotingStrategy):
    """
    At least one methodology must emit a signal.
    If methodologies conflict (e.g. one LONG, one SHORT), the result is FLAT.
    """
    
    def vote(self, evaluations: Sequence[Optional[MethodologyEvaluation]]) -> Optional[MethodologyEvaluation]:
        valid_evals = [e for e in evaluations if e is not None and e.is_active]
        if not valid_evals:
            return None
            
        directions = {e.direction for e in valid_evals if e.direction != 0}
        
        # Combine concepts regardless
        concepts = {}
        for e in valid_evals:
            concepts.update(e.supporting_concepts)
            
        if len(directions) > 1:
            # Conflict! One says Long, one says Short
            return MethodologyEvaluation(
                methodology_id="Composite-Any",
                timestamp=valid_evals[0].timestamp if valid_evals[0].timestamp else datetime.now(timezone.utc),
                is_active=False,
                direction=0,
                confidence=1.0,
                supporting_concepts=concepts,
                metadata={"conflict": True}
            )
            
        if len(directions) == 1:
            direction = directions.pop()
            active = [e for e in valid_evals if e.direction == direction]
            avg_conf = sum(e.confidence for e in active) / len(active)
            return MethodologyEvaluation(
                methodology_id="Composite-Any",
                timestamp=active[0].timestamp if active[0].timestamp else datetime.now(timezone.utc),
                is_active=True,
                direction=direction,
                confidence=avg_conf,
                supporting_concepts=concepts
            )
            
        return None
