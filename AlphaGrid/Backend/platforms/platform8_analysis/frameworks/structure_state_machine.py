from typing import Dict, List, Optional
from Backend.shared_domain.contracts.structure.structure_dtos import (
    StructureStateDTO,
    StructureEventDTO,
    StructureClassificationDTO
)

class InvalidStructureTransitionError(Exception):
    pass

class StructureStateMachine:
    """
    Immutable Finite State Machine governing valid Market Structure transitions.
    """
    
    # Define valid transitions
    # Format: {Current State: [Valid Next States]}
    _transitions: Dict[StructureStateDTO, List[StructureStateDTO]] = {
        StructureStateDTO.BULLISH: [
            StructureStateDTO.PULLBACK, 
            StructureStateDTO.CONSOLIDATION,
            StructureStateDTO.BEARISH # Only via CHOCH/MSS
        ],
        StructureStateDTO.PULLBACK: [
            StructureStateDTO.BULLISH, # Continuation (BOS)
            StructureStateDTO.CONSOLIDATION,
            StructureStateDTO.BEARISH # Failure (CHOCH)
        ],
        StructureStateDTO.BEARISH: [
            StructureStateDTO.PULLBACK, 
            StructureStateDTO.CONSOLIDATION,
            StructureStateDTO.BULLISH # Only via CHOCH/MSS
        ],
        StructureStateDTO.CONSOLIDATION: [
            StructureStateDTO.BULLISH, # Breakout
            StructureStateDTO.BEARISH, # Breakdown
            StructureStateDTO.EXPANSION
        ],
        StructureStateDTO.EXPANSION: [
            StructureStateDTO.PULLBACK,
            StructureStateDTO.CONSOLIDATION
        ]
    }
    
    @classmethod
    def process_event(cls, current_state: StructureStateDTO, event: StructureEventDTO) -> StructureStateDTO:
        """
        Calculates the next state based on the current state and a detected structure event.
        Raises InvalidStructureTransitionError if the resulting transition violates the FSM.
        """
        next_state = cls._determine_next_state(current_state, event)
        
        if next_state not in cls._transitions[current_state] and next_state != current_state:
            raise InvalidStructureTransitionError(
                f"Invalid transition from {current_state.value} to {next_state.value} triggered by {event.id}"
            )
            
        return next_state

    @classmethod
    def _determine_next_state(cls, current_state: StructureStateDTO, event: StructureEventDTO) -> StructureStateDTO:
        """
        Internal mapping of events to state changes.
        """
        # Example mapping logic (will be extended based on registry semantics)
        event_id = event.id.lower()
        
        if "choch" in event_id or "mss" in event_id:
            # Reversal logic
            if current_state in (StructureStateDTO.BULLISH, StructureStateDTO.PULLBACK):
                return StructureStateDTO.BEARISH
            elif current_state == StructureStateDTO.BEARISH:
                return StructureStateDTO.BULLISH
                
        if "bos" in event_id:
            # Continuation logic
            if current_state == StructureStateDTO.PULLBACK:
                # Need HTF context to know if it's Bullish or Bearish continuation.
                # Assuming the event carries context, but for simple FSM we return the prevailing trend.
                # In a real impl, this uses event classification mapping.
                pass 
                
        return current_state
