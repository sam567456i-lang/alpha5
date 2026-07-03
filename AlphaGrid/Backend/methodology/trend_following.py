"""Trend Following Methodology."""

from typing import Dict, Any, List
from datetime import datetime

from Backend.signals.primitive.context import SignalContext
from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation


class TrendFollowingMethodology(AbstractMethodology):
    """
    Evaluates primitive signals through the Trend Following methodology rules.
    """
    
    ENGINE_METADATA = {
        "id": "trend_following_methodology",
        "version": "1.0",
        "family": "Trend Following",
        "produces": ["MethodologyEvaluation"],
        "downstream": "StrategyEngine"
    }

    @classmethod
    def get_name(cls) -> str:
        return "TrendFollowingMethodology"

    def evaluate(self, context: SignalContext) -> MethodologyEvaluation:
        # We look for TREND_LONG, TREND_SHORT, TREND_STRENGTHENING
        trend_signals = [s for s in context.get_all_signals() if "TREND" in s.signal_type]
        momentum_signals = [s for s in context.get_all_signals() if "MOMENTUM" in s.signal_type]
        
        # Get the timestamp from the context if possible, or from a signal
        timestamp = trend_signals[0].timestamp if trend_signals else None
        
        if not trend_signals:
            return MethodologyEvaluation(
                methodology_id=self.get_name(),
                timestamp=timestamp,
                is_active=False,
                direction=0,
                confidence=0.0
            )
            
        # Simple methodology rule: If we have strengthening long, we are aligned.
        is_active = False
        direction = 0
        strength = 0.0
        ids = []
        
        for sig in trend_signals:
            ids.append(sig.id)
            if sig.direction != 0:
                direction = sig.direction
                strength = max(strength, sig.confidence)
                if "STRENGTHENING" in sig.signal_type or "LONG" in sig.signal_type or "SHORT" in sig.signal_type:
                    is_active = True
                    
        for sig in momentum_signals:
            if direction != 0 and sig.direction == -direction:
                is_active = False
                ids.append(sig.id)
                
        return MethodologyEvaluation(
            methodology_id=self.get_name(),
            timestamp=timestamp,
            is_active=is_active,
            direction=direction,
            confidence=strength,
            metadata={"supporting_signals": ids}
        )
