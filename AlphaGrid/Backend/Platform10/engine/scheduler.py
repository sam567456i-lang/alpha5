from typing import Dict, Any
from Backend.Platform10.contracts.dtos import MarketStateDTO

class MethodologyScheduler:
    """Controls the execution cadence of methodologies."""
    
    @staticmethod
    def should_execute(market_state: MarketStateDTO, cap_meta: Dict[str, Any]) -> bool:
        """
        Determines if the methodology should execute on this tick/candle.
        Compares market_state.timeframe against the plugin's supported timeframes.
        """
        supported_timeframes = cap_meta.get("supported_timeframes", [])
        
        if not supported_timeframes:
            # Default behavior if not explicitly constrained
            return True
            
        current_tf = market_state.timeframe
        
        # Capability Negotiation: only run if the current state's timeframe matches the required cadence
        return current_tf in supported_timeframes
