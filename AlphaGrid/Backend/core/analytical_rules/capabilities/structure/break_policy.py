from abc import ABC, abstractmethod
from typing import Dict, Any

class BreakPolicy(ABC):
    """
    Abstract Base Class for defining what geometrically constitutes a structural break.
    This delegates methodology-specific or parameter-specific logic (e.g. close beyond,
    wick beyond, ATR threshold) out of the objective rules.
    """
    @property
    @abstractmethod
    def policy_id(self) -> str:
        pass
        
    @abstractmethod
    def is_break(self, broken_price: float, breaking_price: float, direction: str) -> bool:
        """
        Evaluate whether the breaking_price objectively breaks the broken_price in the given direction.
        In a fully featured implementation, this might take entire nodes or OHLC bars.
        For Wave 2B.1B, we simulate with simple price comparison.
        """
        pass
        
    @abstractmethod
    def get_policy_checksum(self) -> str:
        pass

class DefaultBreakPolicy(BreakPolicy):
    def __init__(self, required_displacement: float = 0.0):
        self.required_displacement = required_displacement

    @property
    def policy_id(self) -> str:
        return f"default_break_{self.required_displacement}"
        
    def is_break(self, broken_price: float, breaking_price: float, direction: str) -> bool:
        if direction == "BULLISH":
            return breaking_price > (broken_price + self.required_displacement)
        elif direction == "BEARISH":
            return breaking_price < (broken_price - self.required_displacement)
        return False
        
    def get_policy_checksum(self) -> str:
        return f"default_break_policy_v1_{self.required_displacement}"
