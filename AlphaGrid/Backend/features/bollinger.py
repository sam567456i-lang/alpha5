"""
Bollinger Bands Features as atomic primitives.

This module provides the Bollinger Bands indicator broken down into its atomic feature primitives:
- BollingerBandsFeature (Upper, Middle, Lower)
- BollingerMetricsFeature (Band Width, %B, Z-Score)
"""

import math
from collections import deque
from typing import Any, Dict, List, Optional
from Shared.models.market import MarketSnapshot
from Backend.features.base import AbstractFeature


class BollingerBandsFeature(AbstractFeature):
    """
    Computes Upper, Middle (SMA), and Lower Bollinger Bands.
    Exposes them as a dictionary for downstream features to consume.
    """

    def __init__(self, period: int = 20, num_std: float = 2.0) -> None:
        """
        Initializes the Bollinger Bands feature.
        
        Args:
            period: The lookback period for the SMA and standard deviation.
            num_std: The number of standard deviations for the bands.
        """
        self.period: int = period
        self.num_std: float = num_std
        self._window: deque[float] = deque(maxlen=self.period)

    @classmethod
    def get_name(cls) -> str:
        """Returns the unique identifier for this feature."""
        return "Bollinger_Bands"

    @classmethod
    def get_version(cls) -> str:
        """Returns the feature version."""
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        """Returns the list of required feature dependencies."""
        return []

    @classmethod
    def warmup_period(cls) -> int:
        """Returns the number of periods required to warm up."""
        return 20

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Optional[Dict[str, float]]:
        """
        Computes the Bollinger Bands.

        Args:
            snapshot: The current market snapshot.
            dependency_values: Dictionary containing required feature values.

        Returns:
            Dictionary containing 'middle', 'upper', 'lower', and 'std_dev', 
            or None if warming up.
        """
        price = float(snapshot.close)
        self._window.append(price)

        if len(self._window) < self.period:
            return None

        mean = sum(self._window) / self.period
        variance = sum((x - mean) ** 2 for x in self._window) / self.period
        std_dev = math.sqrt(variance)

        return {
            "middle": mean,
            "upper": mean + (self.num_std * std_dev),
            "lower": mean - (self.num_std * std_dev),
            "std_dev": std_dev
        }


class BollingerMetricsFeature(AbstractFeature):
    """
    Computes Band Width, %B, and Z-Score based on Bollinger Bands.
    """

    @classmethod
    def get_name(cls) -> str:
        """Returns the unique identifier for this feature."""
        return "Bollinger_Metrics"

    @classmethod
    def get_version(cls) -> str:
        """Returns the feature version."""
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        """Returns the list of required feature dependencies."""
        return ["Bollinger_Bands"]

    @classmethod
    def warmup_period(cls) -> int:
        """Returns the number of periods required to warm up."""
        return 20

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Optional[Dict[str, float]]:
        """
        Computes advanced Bollinger metrics.

        Args:
            snapshot: The current market snapshot.
            dependency_values: Dictionary containing required feature values.

        Returns:
            Dictionary containing 'band_width', 'pct_b', and 'z_score',
            or None if dependencies are warming up.
        """
        bands = dependency_values.get("Bollinger_Bands")
        if bands is None:
            return None
            
        price = float(snapshot.close)
        upper = float(bands["upper"])
        lower = float(bands["lower"])
        middle = float(bands["middle"])
        std_dev = float(bands["std_dev"])
        
        band_width = (upper - lower) / middle if middle != 0 else 0.0
        pct_b = (price - lower) / (upper - lower) if upper != lower else 0.0
        z_score = (price - middle) / std_dev if std_dev != 0 else 0.0
        
        return {
            "band_width": band_width,
            "pct_b": pct_b,
            "z_score": z_score
        }
