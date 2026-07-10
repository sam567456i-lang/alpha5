from dataclasses import dataclass
from typing import List, Optional
from Backend.core.decision.fusion_engine import MarketOpportunity

@dataclass
class TradeIntent:
    """The final actionable payload passed to Platform 13 (Execution)."""
    intent_id: str
    symbol: str
    directional_bias: str
    strategy_type: str # e.g. BREAKOUT, MEAN_REVERSION
    target_position_size_usd: float
    confidence: float
    opportunity_ref: MarketOpportunity
    
class StrategyEngine:
    """Maps a fused MarketOpportunity into a specific Strategy."""
    
    def map_to_strategy(self, opportunity: MarketOpportunity) -> str:
        # Simplistic mapping logic
        if opportunity.directional_bias == "BULLISH" and opportunity.regime_context == "TREND":
            return "TREND_CONTINUATION"
        elif opportunity.directional_bias == "BEARISH" and opportunity.regime_context == "RANGE":
            return "MEAN_REVERSION"
        return "UNKNOWN"
