from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

from Backend.core.methodologies.evidence import MethodologyClaim

@dataclass
class MarketOpportunity:
    """The fused consensus output representing a tradable edge."""
    symbol: str
    timeframe: str
    opportunity_id: str
    directional_bias: str # BULLISH, BEARISH, NEUTRAL
    aggregate_confidence: float
    supporting_claims: List[MethodologyClaim]
    contradicting_claims: List[MethodologyClaim]
    regime_context: str

class DecisionFusionEngine:
    """Fuses competing MethodologyClaims into actionable MarketOpportunities."""
    
    def fuse_claims(self, claims: List[MethodologyClaim], symbol: str, timeframe: str, regime: str) -> MarketOpportunity:
        # Simplistic fusion logic for demonstration
        bullish_claims = [c for c in claims if "Bullish" in c.claim_type]
        bearish_claims = [c for c in claims if "Bearish" in c.claim_type]
        
        bullish_conf = sum(c.confidence_vector.confidence for c in bullish_claims)
        bearish_conf = sum(c.confidence_vector.confidence for c in bearish_claims)
        
        bias = "BULLISH" if bullish_conf > bearish_conf else "BEARISH" if bearish_conf > bullish_conf else "NEUTRAL"
        agg_conf = max(bullish_conf, bearish_conf) / (len(claims) if claims else 1)
        
        return MarketOpportunity(
            symbol=symbol,
            timeframe=timeframe,
            opportunity_id=f"opp_{int(datetime.now().timestamp())}",
            directional_bias=bias,
            aggregate_confidence=agg_conf,
            supporting_claims=bullish_claims if bias == "BULLISH" else bearish_claims,
            contradicting_claims=bearish_claims if bias == "BULLISH" else bullish_claims,
            regime_context=regime
        )
