from typing import Dict, List, Type, Any
from Backend.platforms.platform8_analysis.plugin_framework import AnalysisPlugin
from Backend.platforms.platform8_analysis.geometry_states import (
    GeometryInputDTO, SwingState, TimeExtremesState, RangeState,
    SupportResistanceState, TrendlineState, ChannelState, CompressionExpansionState
)
from Backend.core.state import BaseState, ExecutionContext

class GeometryPlugin(AnalysisPlugin):
    """
    Geometry Plugin
    Responsible for deterministic price action geometry: Swings, Time Extremes, Ranges.
    """
    
    @property
    def family_name(self) -> str:
        return "Geometry"

    @property
    def supported_markets(self) -> List[str]:
        return ["NSE_Index_Options", "NSE_Futures", "NSE_Cash"]
        
    def register_states(self) -> Dict[str, Type[BaseState]]:
        return {
            "ANA_PRICE_ACTION_SWING": SwingState,
            "ANA_PRICE_ACTION_TIME_EXTREMES": TimeExtremesState,
            "ANA_PRICE_ACTION_RANGE": RangeState,
            "ANA_PRICE_ACTION_SUPPORT_RESISTANCE": SupportResistanceState,
            "ANA_PRICE_ACTION_TRENDLINE": TrendlineState,
            "ANA_PRICE_ACTION_CHANNEL": ChannelState,
            "ANA_PRICE_ACTION_COMPRESSION_EXPANSION": CompressionExpansionState
        }
        
    def execute(self, inputs: Dict[str, Any], context: ExecutionContext) -> Dict[str, BaseState]:
        # Extract inputs
        input_dto: GeometryInputDTO = inputs.get("geometry_input")
        
        # Calculate next states deterministically
        next_swing = SwingState.calculate_next(inputs.get("previous_swing_state"), input_dto, context)
        next_extremes = TimeExtremesState.calculate_next(inputs.get("previous_extremes_state"), input_dto, context)
        next_range = RangeState.calculate_next(inputs.get("previous_range_state"), input_dto, context)
        next_sr = SupportResistanceState.calculate_next(inputs.get("previous_sr_state"), input_dto, context)
        next_tl = TrendlineState.calculate_next(inputs.get("previous_tl_state"), input_dto, context)
        next_ch = ChannelState.calculate_next(inputs.get("previous_ch_state"), input_dto, context)
        next_ce = CompressionExpansionState.calculate_next(inputs.get("previous_ce_state"), input_dto, context)
        
        return {
            "ANA_PRICE_ACTION_SWING": next_swing,
            "ANA_PRICE_ACTION_TIME_EXTREMES": next_extremes,
            "ANA_PRICE_ACTION_RANGE": next_range,
            "ANA_PRICE_ACTION_SUPPORT_RESISTANCE": next_sr,
            "ANA_PRICE_ACTION_TRENDLINE": next_tl,
            "ANA_PRICE_ACTION_CHANNEL": next_ch,
            "ANA_PRICE_ACTION_COMPRESSION_EXPANSION": next_ce
        }
