from typing import List, Dict, Any
from Backend.Platform12.contracts.dtos import OpportunityDetectionDTO, OpportunityLifecycle
from Backend.Platform12.evaluators.base import AbstractOpportunityEvaluator

class TrendOpportunityEvaluator(AbstractOpportunityEvaluator):
    @property
    def evaluator_id(self) -> str:
        return "cap_evaluator_trend_opportunity"
        
    @property
    def required_methodologies(self) -> List[str]:
        return ["Trend"]
        
    @property
    def supported_markets(self) -> List[str]:
        return ["Crypto", "Equities", "Forex"]
        
    @property
    def supported_timeframes(self) -> List[str]:
        return ["*"]
        
    @property
    def produces_opportunity_types(self) -> List[str]:
        return ["Trend Continuation", "Trend Reversal"]
        
    def evaluate(self, composite_context: Any, profile: Dict[str, Any]) -> List[OpportunityDetectionDTO]:
        opportunities = []
        
        # Example evaluation logic reading from composite_context (mocking the context interface)
        intent = getattr(composite_context, 'numerical_intent', 0.0)
        consensus = getattr(composite_context, 'consensus', 0.0)
        
        required_intent = profile.get("required_consensus", 0.7)
        
        if abs(intent) >= required_intent and consensus >= required_intent:
            direction = "Bullish" if intent > 0 else "Bearish"
            opp = OpportunityDetectionDTO(
                opportunity_type="Trend Continuation",
                direction=direction,
                exists=True,
                market=getattr(composite_context, 'market', 'UNKNOWN'),
                symbol=getattr(composite_context, 'symbol', 'UNKNOWN'),
                timeframe=getattr(composite_context, 'timeframe', 'UNKNOWN'),
                strength=abs(intent),
                confidence=consensus,
                lifecycle=OpportunityLifecycle.DETECTED,
                opportunity_context=f"Strong {direction} trend momentum matches the consensus threshold.",
                category="Momentum"
            )
            # Add trace
            opp.trace.evaluator_id = self.evaluator_id
            opp.trace.composite_decision_context_id = getattr(composite_context, 'id', None)
            opp.derived_from = opp.trace.composite_decision_context_id
            
            opportunities.append(opp)
            
        return opportunities
