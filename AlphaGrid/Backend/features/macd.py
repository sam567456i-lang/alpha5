"""
MACD Features as atomic primitives.

This module provides the MACD (Moving Average Convergence Divergence) indicator
broken down into its atomic feature primitives:
- EMA12Feature
- EMA26Feature
- MACDLineFeature (EMA12 - EMA26)
- MACDSignalFeature (9-period EMA of MACD Line)
- MACDHistogramFeature (MACD Line - MACD Signal)
"""

from typing import Any, Dict, List, Optional
from Shared.models.market import MarketSnapshot
from Backend.features.base import AbstractFeature
from Backend.features.trend import EMAFeature


class EMA12Feature(EMAFeature):
    """
    Computes an Exponential Moving Average (EMA) over a 12-period window.
    Subclasses the base EMAFeature for standard MACD configuration.
    """

    def __init__(self) -> None:
        """Initializes the EMA 12 feature."""
        super().__init__(period=12)

    @classmethod
    def get_name(cls) -> str:
        """Returns the unique identifier for this feature."""
        return "EMA_12"

    @classmethod
    def warmup_period(cls) -> int:
        """Returns the number of periods required to warm up the EMA."""
        return 12


class EMA26Feature(EMAFeature):
    """
    Computes an Exponential Moving Average (EMA) over a 26-period window.
    Subclasses the base EMAFeature for standard MACD configuration.
    """

    def __init__(self) -> None:
        """Initializes the EMA 26 feature."""
        super().__init__(period=26)

    @classmethod
    def get_name(cls) -> str:
        """Returns the unique identifier for this feature."""
        return "EMA_26"

    @classmethod
    def warmup_period(cls) -> int:
        """Returns the number of periods required to warm up the EMA."""
        return 26


class MACDLineFeature(AbstractFeature):
    """
    Computes the MACD Line (EMA_12 - EMA_26).
    """

    @classmethod
    def get_name(cls) -> str:
        """Returns the unique identifier for this feature."""
        return "MACD_Line"

    @classmethod
    def get_version(cls) -> str:
        """Returns the feature version."""
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        """Returns the list of required feature dependencies."""
        return ["EMA_12", "EMA_26"]

    @classmethod
    def warmup_period(cls) -> int:
        """
        Returns the number of periods required to warm up.
        Governed by the longest dependency (EMA_26).
        """
        return 26

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Optional[float]:
        """
        Computes the MACD Line.

        Args:
            snapshot: The current market snapshot.
            dependency_values: Dictionary containing required feature values.

        Returns:
            The computed MACD Line, or None if dependencies are warming up.
        """
        ema12 = dependency_values.get("EMA_12")
        ema26 = dependency_values.get("EMA_26")
        
        if ema12 is None or ema26 is None:
            return None
            
        return float(ema12 - ema26)


class MACDSignalFeature(AbstractFeature):
    """
    Computes the MACD Signal Line (9-period EMA of the MACD Line).
    """

    def __init__(self) -> None:
        """Initializes the MACD Signal feature."""
        self.period: int = 9
        self.alpha: float = 2.0 / (self.period + 1.0)
        self._ema: Optional[float] = None
        self._buffer: List[float] = []
        self._initialized: bool = False

    @classmethod
    def get_name(cls) -> str:
        """Returns the unique identifier for this feature."""
        return "MACD_Signal"

    @classmethod
    def get_version(cls) -> str:
        """Returns the feature version."""
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        """Returns the list of required feature dependencies."""
        return ["MACD_Line"]

    @classmethod
    def warmup_period(cls) -> int:
        """
        Returns the number of periods required to warm up.
        26 (MACD Line) + 9 (Signal) = 35 periods total.
        """
        return 35

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Optional[float]:
        """
        Computes the MACD Signal Line.

        Args:
            snapshot: The current market snapshot.
            dependency_values: Dictionary containing required feature values.

        Returns:
            The computed MACD Signal Line, or None if warming up.
        """
        macd_line = dependency_values.get("MACD_Line")
        if macd_line is None:
            return None
            
        macd_line = float(macd_line)
        
        if not self._initialized:
            self._buffer.append(macd_line)
            if len(self._buffer) == self.period:
                self._ema = sum(self._buffer) / self.period
                self._initialized = True
            return None
            
        if self._ema is not None:
            self._ema = (macd_line - self._ema) * self.alpha + self._ema
            
        return self._ema


class MACDHistogramFeature(AbstractFeature):
    """
    Computes the MACD Histogram (MACD Line - MACD Signal Line).
    """

    @classmethod
    def get_name(cls) -> str:
        """Returns the unique identifier for this feature."""
        return "MACD_Histogram"

    @classmethod
    def get_version(cls) -> str:
        """Returns the feature version."""
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        """Returns the list of required feature dependencies."""
        return ["MACD_Line", "MACD_Signal"]

    @classmethod
    def warmup_period(cls) -> int:
        """
        Returns the number of periods required to warm up.
        Matches the MACD Signal Line warmup (35).
        """
        return 35

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Optional[float]:
        """
        Computes the MACD Histogram.

        Args:
            snapshot: The current market snapshot.
            dependency_values: Dictionary containing required feature values.

        Returns:
            The computed MACD Histogram, or None if dependencies are warming up.
        """
        macd_line = dependency_values.get("MACD_Line")
        macd_sig = dependency_values.get("MACD_Signal")
        
        if macd_line is None or macd_sig is None:
            return None
            
        return float(macd_line - macd_sig)
