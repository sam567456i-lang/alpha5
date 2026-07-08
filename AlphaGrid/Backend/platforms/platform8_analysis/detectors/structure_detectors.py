from typing import Any, Dict
from Backend.platforms.platform8_analysis.frameworks.structure_detector_base import StructureDetectorBase
from Backend.shared_domain.contracts.structure.structure_dtos import (
    StructureEventDTO,
    StructureStateDTO,
    StructureClassificationDTO,
    StructureObjectDTO
)
from Backend.platforms.platform8_analysis.frameworks.structure_state_machine import StructureStateMachine
from Backend.price_geometry.objects import Swing

class InvalidStructureInputError(Exception):
    pass

class GenericStructureDetector(StructureDetectorBase):
    """
    Dynamic Structure Detector driven purely by the capability registry.
    Handles BOS, CHOCH, MSS, Swings, etc. via configuration.
    Strictly enforces Swing Ownership (no price data accepted directly).
    """
    
    def __init__(self, capability_def: dict):
        self.capability_id = capability_def.get("id")
        self.config = capability_def.get("config", {})
        self.state_machine = StructureStateMachine()
        
    def validate_structure_context(self, inputs: Dict[str, Any]) -> bool:
        """
        Ensures the pre-requisite structure objects (e.g. Swings for BOS detection) exist.
        Strictly rejects PriceDTO.
        """
        if "price" in inputs or "PriceDTO" in inputs:
            raise InvalidStructureInputError(f"Detector {self.capability_id} cannot consume raw price data. Provide a SwingDTO.")
            
        required_objects = self.config.get("requires_geometry", [])
        for req in required_objects:
            if req not in inputs:
                return False
                
        # Validate that if a swing is provided, it's actually a Swing object
        if "swing" in inputs and not isinstance(inputs["swing"], Swing):
             raise InvalidStructureInputError("The provided 'swing' is not a valid Swing object.")
             
        return True
        
    def evaluate(self, inputs: Dict[str, Any], state: Dict[str, Any]) -> Any:
        """
        Evaluates the structure configuration against current inputs.
        Delegates state transitions to the StructureStateMachine.
        """
        if not self.validate_structure_context(inputs):
            return None
            
        # 1. Detect structural condition based on registry logic
        detection_type = self.config.get("detection_type")
        
        # 2. Extract geometries
        # Notice we are extracting from a Swing, NOT a Price!
        source_swing: Swing = inputs.get("swing")
        if not source_swing:
            return None # Must have a swing to evaluate structure
            
        current_price = source_swing.price
        
        # This is a stub for the generic logic which would normally read from 
        # previous states and compare against swing extremes.
        event_detected = False
        is_internal = False
        is_confirmed = False
        
        if detection_type == "BOS":
            event_detected = True 
            is_confirmed = inputs.get("is_confirmed", True) # Example hook
            is_internal = source_swing.is_internal
        elif detection_type == "CHOCH":
            event_detected = True
            is_confirmed = inputs.get("is_confirmed", True)
            is_internal = source_swing.is_internal
            
        if not event_detected:
            return None
            
        # 3. Create Event DTO
        event_dto = StructureEventDTO(
            id=self.capability_id,
            timestamp=source_swing.timestamp, # Tie timestamp to the swing
            consumes=self.config.get("consumes", []),
            produces=self.config.get("produces", []),
            event_price=current_price,
            is_internal=is_internal,
            is_confirmed=is_confirmed,
            sequence_number=inputs.get("sequence_number", 0) # Passed down by engine
        )
        
        # 4. Enforce State Transition
        current_context = state.get("structure_context")
        if not current_context:
            return event_dto
            
        next_context = self.state_machine.process_event(current_context, event_dto)
        
        return {
            "event": event_dto,
            "next_context": next_context
        }
