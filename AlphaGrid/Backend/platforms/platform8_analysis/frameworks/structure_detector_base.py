from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
from Backend.platforms.platform8_analysis.frameworks.concept_detector_base import ConceptDetectorBase
from Backend.shared_domain.contracts.structure.structure_dtos import (
    StructureClassificationDTO,
    StructureStateDTO,
    StructureObjectDTO,
    StructureEventDTO,
    StructureContextDTO
)

class StructureDetectorBase(ConceptDetectorBase):
    """
    Base class specifically for Market Structure Detectors (CHoCH, BOS, Swings).
    Provides built-in methods for multi-timeframe alignment checks and state machine hooks.
    """
    
    @abstractmethod
    def validate_structure_context(self, inputs: Dict[str, Any]) -> bool:
        """
        Validates that required geometry (e.g. valid swings) is present
        before executing structure detection.
        """
        pass
    
    def enforce_state_transition(self, current_state: StructureStateDTO, event: StructureEventDTO) -> StructureStateDTO:
        """
        Hook into the Structure State Machine to determine the next state.
        This ensures structure evaluation is strictly stateful.
        """
        # This will be fully delegated to the StructureStateMachine in the implementation.
        pass
