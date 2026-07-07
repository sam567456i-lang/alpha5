from typing import Any, Dict
from Backend.platforms.platform8_analysis.frameworks.structure_detector_base import StructureDetectorBase
from Backend.shared_domain.contracts.structure.structure_dtos import (
    StructureEventDTO,
    StructureStateDTO,
    StructureClassificationDTO
)
from Backend.platforms.platform8_analysis.frameworks.structure_state_machine import StructureStateMachine

class GenericStructureDetector(StructureDetectorBase):
    """
    Dynamic Structure Detector driven purely by the capability registry.
    Handles BOS, CHOCH, MSS, Swings, etc. via configuration, rather than specific subclasses.
    """
    
    def __init__(self, capability_def: dict):
        # Expected to receive the semantic definition from capability_registry.yaml
        self.capability_id = capability_def.get("id")
        self.config = capability_def.get("config", {})
        self.state_machine = StructureStateMachine()
        
    def validate_structure_context(self, inputs: Dict[str, Any]) -> bool:
        """
        Ensures the pre-requisite structure objects (e.g. Swings for BOS detection) exist.
        """
        required_objects = self.config.get("requires_geometry", [])
        for req in required_objects:
            if req not in inputs:
                return False
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
        current_price = inputs.get("price", 0.0)
        
        # This is a stub for the generic logic which would normally read from 
        # previous states and compare against swing extremes.
        event_detected = False
        if detection_type == "BREAK_OF_STRUCTURE":
            # Logic to verify price crossed the previous structural swing in direction of trend
            event_detected = True 
        elif detection_type == "CHANGE_OF_CHARACTER":
            # Logic to verify price crossed previous opposing swing
            event_detected = True
            
        if not event_detected:
            return None
            
        # 3. Create Event DTO
        event_dto = StructureEventDTO(
            id=self.capability_id,
            timestamp=inputs.get("timestamp"),
            consumes=self.config.get("consumes", []),
            produces=self.config.get("produces", []),
            event_price=current_price,
            is_internal=self.config.get("is_internal", False)
        )
        
        # 4. Enforce State Transition
        current_trend = inputs.get("current_trend_state", StructureStateDTO.CONSOLIDATION)
        next_trend = self.state_machine.process_event(current_trend, event_dto)
        
        return event_dto
