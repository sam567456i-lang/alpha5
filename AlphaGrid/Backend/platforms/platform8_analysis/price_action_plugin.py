from typing import Dict, List, Type, Any
from Backend.platforms.platform8_analysis.plugin_framework import AnalysisPlugin
from Backend.platforms.platform8_analysis.price_action_states import (
    CandlestickInputDTO, CandlestickState, EngulfingState,
    PinBarState, InsideOutsideBarState, MarubozuDojiState
)
from Backend.core.state import BaseState, ExecutionContext

class PriceActionPlugin(AnalysisPlugin):
    """
    Price Action Plugin
    Responsible for deterministic candlestick patterns.
    """
    
    @property
    def family_name(self) -> str:
        return "Price Action"

    @property
    def supported_markets(self) -> List[str]:
        return ["NSE_Index_Options", "NSE_Futures", "NSE_Cash"]
        
    def register_states(self) -> Dict[str, Type[BaseState]]:
        return {
            "ANA_PRICE_ACTION_CANDLESTICK": CandlestickState,
            "ANA_PRICE_ACTION_ENGULFING": EngulfingState,
            "ANA_PRICE_ACTION_PINBAR": PinBarState,
            "ANA_PRICE_ACTION_INSIDE_OUTSIDE": InsideOutsideBarState,
            "ANA_PRICE_ACTION_MARUBOZU_DOJI": MarubozuDojiState
        }
        
    def execute(self, inputs: Dict[str, Any], context: ExecutionContext) -> Dict[str, BaseState]:
        # Extract inputs
        input_dto: CandlestickInputDTO = inputs.get("candlestick_input")
        
        # Calculate next states deterministically
        next_candle = CandlestickState.calculate_next(inputs.get("previous_candle_state"), input_dto, context)
        next_engulfing = EngulfingState.calculate_next(inputs.get("previous_engulfing_state"), input_dto, context)
        next_pinbar = PinBarState.calculate_next(inputs.get("previous_pinbar_state"), input_dto, context)
        next_inout = InsideOutsideBarState.calculate_next(inputs.get("previous_inout_state"), input_dto, context)
        next_marudoji = MarubozuDojiState.calculate_next(inputs.get("previous_marudoji_state"), input_dto, context)
        
        return {
            "ANA_PRICE_ACTION_CANDLESTICK": next_candle,
            "ANA_PRICE_ACTION_ENGULFING": next_engulfing,
            "ANA_PRICE_ACTION_PINBAR": next_pinbar,
            "ANA_PRICE_ACTION_INSIDE_OUTSIDE": next_inout,
            "ANA_PRICE_ACTION_MARUBOZU_DOJI": next_marudoji
        }
