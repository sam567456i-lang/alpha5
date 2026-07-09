from abc import ABC, abstractmethod
from typing import Dict, Any

class ShiftPolicy(ABC):
    """
    Abstract Base Class for defining what constitutes a structural shift.
    This dictates whether a TrendReversalEvent satisfies the criteria to escalate 
    into a StructuralShiftEvent (e.g. minimum_breaks, minimum_time, minimum_leg_length).
    """
    @property
    @abstractmethod
    def policy_id(self) -> str:
        pass
        
    @abstractmethod
    def is_shift(self, reversal_event_id: str, historical_breaks: int, current_leg_length: float) -> bool:
        """
        Evaluate whether the current context objectively satisfies a structural shift.
        """
        pass
        
    @abstractmethod
    def get_policy_checksum(self) -> str:
        pass

class DefaultShiftPolicy(ShiftPolicy):
    def __init__(self, minimum_breaks: int = 1, minimum_leg_length: float = 0.0):
        self.minimum_breaks = minimum_breaks
        self.minimum_leg_length = minimum_leg_length

    @property
    def policy_id(self) -> str:
        return f"default_shift_{self.minimum_breaks}_{self.minimum_leg_length}"
        
    def is_shift(self, reversal_event_id: str, historical_breaks: int, current_leg_length: float) -> bool:
        return historical_breaks >= self.minimum_breaks and current_leg_length >= self.minimum_leg_length
        
    def get_policy_checksum(self) -> str:
        return f"default_shift_policy_v1_{self.minimum_breaks}_{self.minimum_leg_length}"
