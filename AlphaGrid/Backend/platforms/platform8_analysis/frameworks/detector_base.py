from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
from datetime import datetime

from Backend.core.state import BaseState, ExecutionContext
from Backend.shared_domain.contracts.dtos import LineageDTO

class DetectorBase(ABC):
    """
    Abstract Base Class for all Platform 8 Detectors.
    Enforces that all detectors produce a mathematically deterministic BaseState
    and attach a required LineageDTO.
    """
    
    @property
    @abstractmethod
    def capability_id(self) -> str:
        """The Governance Registry Capability ID this detector implements."""
        pass
        
    @property
    @abstractmethod
    def state_class(self) -> Type[BaseState]:
        """The specific BaseState class this detector produces."""
        pass
        
    @abstractmethod
    def detect(self, inputs: Dict[str, Any], context: ExecutionContext, previous_state: Optional[BaseState]) -> BaseState:
        """
        Core detection logic. Must be purely deterministic.
        Must return an instance of `self.state_class`.
        """
        pass
        
    def execute(self, inputs: Dict[str, Any], context: ExecutionContext, previous_state: Optional[BaseState]) -> BaseState:
        """
        Wrapper that enforces LineageDTO injection and validation.
        """
        state = self.detect(inputs, context, previous_state)
        
        # Enforce LineageDTO
        if not state.lineage:
            raise ValueError(f"Detector {self.capability_id} failed to attach a LineageDTO to its state.")
            
        return state
