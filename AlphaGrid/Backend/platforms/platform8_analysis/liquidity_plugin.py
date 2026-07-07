from typing import Dict, List, Type, Any
from Backend.platforms.platform8_analysis.plugin_framework import AnalysisPlugin
from Backend.platforms.platform8_analysis.liquidity_states import (
    LiquidityInputDTO, LiquidityState, SweepState, StopHuntState
)
from Backend.core.state import BaseState, ExecutionContext

class LiquidityPlugin(AnalysisPlugin):
    """
    Liquidity Plugin
    Responsible for identifying Liquidity Pools, Sweeps, Stop Hunts, and Internal/External Liquidity.
    Must build strictly on top of Geometry plugin outputs.
    """
    
    @property
    def family_name(self) -> str:
        return "Liquidity"

    @property
    def supported_markets(self) -> List[str]:
        return ["NSE_Index_Options", "NSE_Futures", "NSE_Cash"]
        
    def register_states(self) -> Dict[str, Type[BaseState]]:
        return {
            "ANA_MARKET_CONTEXT_LIQUIDITY_POOLS": LiquidityState,
            "ANA_MARKET_CONTEXT_SWEEPS": SweepState,
            "ANA_MARKET_CONTEXT_STOP_HUNTS": StopHuntState
        }
        
    def execute(self, inputs: Dict[str, Any], context: ExecutionContext) -> Dict[str, BaseState]:
        # Extract inputs
        input_dto: LiquidityInputDTO = inputs.get("liquidity_input")
        
        # Calculate next states deterministically
        next_liq = LiquidityState.calculate_next(inputs.get("previous_liquidity_state"), input_dto, context)
        next_sweep = SweepState.calculate_next(inputs.get("previous_sweep_state"), input_dto, context)
        next_hunt = StopHuntState.calculate_next(inputs.get("previous_hunt_state"), input_dto, context)
        
        return {
            "ANA_MARKET_CONTEXT_LIQUIDITY_POOLS": next_liq,
            "ANA_MARKET_CONTEXT_SWEEPS": next_sweep,
            "ANA_MARKET_CONTEXT_STOP_HUNTS": next_hunt
        }
