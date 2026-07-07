from typing import Dict, List, Type, Any
from Backend.platforms.platform8_analysis.plugin_framework import AnalysisPlugin
from Backend.platforms.platform8_analysis.market_structure_states import (
    MarketStructureInputDTO, BreakOfStructureState, ChangeOfCharacterState,
    MarketStructureShiftState, InternalExternalStructureState
)
from Backend.core.state import BaseState, ExecutionContext

class MarketStructurePlugin(AnalysisPlugin):
    """
    Market Structure Plugin
    Responsible for identifying BOS, CHOCH, MSS, and Internal/External Structure.
    Must build strictly on top of Geometry plugin outputs (Swing States).
    """
    
    @property
    def family_name(self) -> str:
        return "Market Structure"

    @property
    def supported_markets(self) -> List[str]:
        return ["NSE_Index_Options", "NSE_Futures", "NSE_Cash"]
        
    def register_states(self) -> Dict[str, Type[BaseState]]:
        return {
            "ANA_MARKET_STRUCTURE_BOS": BreakOfStructureState,
            "ANA_MARKET_STRUCTURE_CHOCH": ChangeOfCharacterState,
            "ANA_MARKET_STRUCTURE_MSS": MarketStructureShiftState,
            "ANA_MARKET_STRUCTURE_INTERNAL_EXTERNAL": InternalExternalStructureState
        }
        
    def execute(self, inputs: Dict[str, Any], context: ExecutionContext) -> Dict[str, BaseState]:
        # Extract inputs
        input_dto: MarketStructureInputDTO = inputs.get("market_structure_input")
        
        # Calculate next states deterministically
        next_bos = BreakOfStructureState.calculate_next(inputs.get("previous_bos_state"), input_dto, context)
        next_choch = ChangeOfCharacterState.calculate_next(inputs.get("previous_choch_state"), input_dto, context)
        next_mss = MarketStructureShiftState.calculate_next(inputs.get("previous_mss_state"), input_dto, context)
        next_ie = InternalExternalStructureState.calculate_next(inputs.get("previous_ie_state"), input_dto, context)
        
        return {
            "ANA_MARKET_STRUCTURE_BOS": next_bos,
            "ANA_MARKET_STRUCTURE_CHOCH": next_choch,
            "ANA_MARKET_STRUCTURE_MSS": next_mss,
            "ANA_MARKET_STRUCTURE_INTERNAL_EXTERNAL": next_ie
        }
