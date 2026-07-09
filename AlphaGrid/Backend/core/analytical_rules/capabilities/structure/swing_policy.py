from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import json
import hashlib

class SwingPolicy(ABC):
    """
    Abstract Base Class defining the rules for geometric swing node identification.
    Keeps the SwingDetector agnostic of methodology-specific pivoting algorithms.
    """

    @abstractmethod
    def is_swing_high(self, index: int, ohlcv_data: List[Dict[str, Any]]) -> bool:
        """Determines if the candle at the given index forms a valid swing high."""
        pass

    @abstractmethod
    def is_swing_low(self, index: int, ohlcv_data: List[Dict[str, Any]]) -> bool:
        """Determines if the candle at the given index forms a valid swing low."""
        pass

    @property
    @abstractmethod
    def configuration(self) -> Dict[str, Any]:
        """Returns the configuration parameters of this policy for event tagging."""
        pass

    @property
    @abstractmethod
    def policy_id(self) -> str:
        """Returns the unique string identifier for this policy type."""
        pass

    @property
    def policy_checksum(self) -> str:
        """Returns a stable SHA-256 hash of the canonical JSON representation of the configuration."""
        canonical_json = json.dumps(self.configuration, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

class FractalSwingPolicy(SwingPolicy):
    """
    Detects swing nodes based on a strict N-bar fractal configuration.
    """
    def __init__(
        self,
        left_confirmation: int = 2,
        right_confirmation: int = 2,
        equal_high_policy: str = "strict",
        equal_low_policy: str = "strict",
        inside_bar_policy: str = "ignore",
        outside_bar_policy: str = "include"
    ):
        self.left_confirmation = left_confirmation
        self.right_confirmation = right_confirmation
        self.equal_high_policy = equal_high_policy
        self.equal_low_policy = equal_low_policy
        self.inside_bar_policy = inside_bar_policy
        self.outside_bar_policy = outside_bar_policy

    def is_swing_high(self, index: int, ohlcv_data: List[Dict[str, Any]]) -> bool:
        """
        A standard fractal high requires N left bars to have a lower/equal high,
        and N right bars to have a lower/equal high.
        Note: Exact equal-high handling depends on the equal_high_policy.
        """
        if index < self.left_confirmation or index > len(ohlcv_data) - 1 - self.right_confirmation:
            return False
            
        target_high = ohlcv_data[index]["high"]
        
        # Check left
        for i in range(1, self.left_confirmation + 1):
            left_high = ohlcv_data[index - i]["high"]
            if left_high > target_high:
                return False
            if left_high == target_high and self.equal_high_policy == "strict":
                return False
                
        # Check right
        for i in range(1, self.right_confirmation + 1):
            right_high = ohlcv_data[index + i]["high"]
            if right_high > target_high:
                return False
            if right_high == target_high and self.equal_high_policy == "strict":
                return False
                
        return True

    def is_swing_low(self, index: int, ohlcv_data: List[Dict[str, Any]]) -> bool:
        """
        A standard fractal low requires N left bars to have a higher/equal low,
        and N right bars to have a higher/equal low.
        """
        if index < self.left_confirmation or index > len(ohlcv_data) - 1 - self.right_confirmation:
            return False
            
        target_low = ohlcv_data[index]["low"]
        
        # Check left
        for i in range(1, self.left_confirmation + 1):
            left_low = ohlcv_data[index - i]["low"]
            if left_low < target_low:
                return False
            if left_low == target_low and self.equal_low_policy == "strict":
                return False
                
        # Check right
        for i in range(1, self.right_confirmation + 1):
            right_low = ohlcv_data[index + i]["low"]
            if right_low < target_low:
                return False
            if right_low == target_low and self.equal_low_policy == "strict":
                return False
                
        return True
        
    @property
    def configuration(self) -> Dict[str, Any]:
        return {
            "policy": "Fractal",
            "left_confirmation": self.left_confirmation,
            "right_confirmation": self.right_confirmation,
            "equal_high_policy": self.equal_high_policy,
            "equal_low_policy": self.equal_low_policy,
            "inside_bar_policy": self.inside_bar_policy,
            "outside_bar_policy": self.outside_bar_policy
        }

    @property
    def policy_id(self) -> str:
        return "FractalSwingPolicy"

class ZigZagSwingPolicy(SwingPolicy):
    """Placeholder for ZigZag methodology."""
    def is_swing_high(self, index: int, ohlcv_data: List[Dict[str, Any]]) -> bool: pass
    def is_swing_low(self, index: int, ohlcv_data: List[Dict[str, Any]]) -> bool: pass
    @property
    def configuration(self) -> Dict[str, Any]: return {"policy": "ZigZag"}
    @property
    def policy_id(self) -> str: return "ZigZagSwingPolicy"

class ATRSwingPolicy(SwingPolicy):
    """Placeholder for Average True Range methodology."""
    def is_swing_high(self, index: int, ohlcv_data: List[Dict[str, Any]]) -> bool: pass
    def is_swing_low(self, index: int, ohlcv_data: List[Dict[str, Any]]) -> bool: pass
    @property
    def configuration(self) -> Dict[str, Any]: return {"policy": "ATR"}
    @property
    def policy_id(self) -> str: return "ATRSwingPolicy"

class VolatilitySwingPolicy(SwingPolicy):
    """Placeholder for Volatility methodology."""
    def is_swing_high(self, index: int, ohlcv_data: List[Dict[str, Any]]) -> bool: pass
    def is_swing_low(self, index: int, ohlcv_data: List[Dict[str, Any]]) -> bool: pass
    @property
    def configuration(self) -> Dict[str, Any]: return {"policy": "Volatility"}
    @property
    def policy_id(self) -> str: return "VolatilitySwingPolicy"

class AdaptiveSwingPolicy(SwingPolicy):
    """Placeholder for Adaptive methodology."""
    def is_swing_high(self, index: int, ohlcv_data: List[Dict[str, Any]]) -> bool: pass
    def is_swing_low(self, index: int, ohlcv_data: List[Dict[str, Any]]) -> bool: pass
    @property
    def configuration(self) -> Dict[str, Any]: return {"policy": "Adaptive"}
    @property
    def policy_id(self) -> str: return "AdaptiveSwingPolicy"
