"""Standardized Output Protocols for Features."""

from typing import Protocol
from Shared.enums.signal_direction import SignalDirection

class TrendFeatureOutput(Protocol):
    """
    Protocol for any trend-identifying feature output (e.g., EMA, MACD, SuperTrend).
    Ensures that concept generators can consume trend properties uniformly.
    """
    @property
    def direction(self) -> SignalDirection:
        """The identified direction of the trend."""
        ...
