from typing import List, Optional
from Backend.core.decision.fusion_engine import MarketOpportunity
from Backend.core.decision.trade_intent import TradeIntent, StrategyEngine

class RiskEngine:
    """Applies draconian portfolio risk overlays and position sizing."""
    
    def __init__(self, max_portfolio_risk_usd: float):
        self.max_portfolio_risk_usd = max_portfolio_risk_usd
        self.strategy_engine = StrategyEngine()
        
    def evaluate_opportunity(self, opp: MarketOpportunity) -> Optional[TradeIntent]:
        # 1. Base Strategy Mapping
        strategy = self.strategy_engine.map_to_strategy(opp)
        if strategy == "UNKNOWN":
            return None
            
        # 2. Risk Overlays (Mocked)
        if opp.aggregate_confidence < 0.6:
            return None # Fails minimum confidence threshold
            
        # 3. Position Sizing
        # Mocking a fractional Kelly / Volatility adjusted size
        target_size = self.max_portfolio_risk_usd * opp.aggregate_confidence * 0.1
        
        # 4. Generate Intent
        return TradeIntent(
            intent_id=f"int_{opp.opportunity_id}",
            symbol=opp.symbol,
            directional_bias=opp.directional_bias,
            strategy_type=strategy,
            target_position_size_usd=target_size,
            confidence=opp.aggregate_confidence,
            opportunity_ref=opp
        )
