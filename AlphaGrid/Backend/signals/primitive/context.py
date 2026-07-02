"""Primitive Signal Context.

Provides a structured, strongly typed access pattern for Methodologies 
to retrieve PrimitiveSignals evaluated on specific timeframes.
"""

from typing import Dict, Tuple, List
from collections import defaultdict
from Backend.signals.primitive.base import PrimitiveSignal

class SignalContext:
    """
    Immutable collection of PrimitiveSignals evaluated for a specific market event.
    Replaces Concept-based Methodologies with Signal-based Methodologies.
    """

    def __init__(self, signals: Tuple[PrimitiveSignal, ...]) -> None:
        self._signals = signals
        self._index: Dict[str, List[PrimitiveSignal]] = defaultdict(list)
        for s in signals:
            self._index[s.id].append(s)

    def get_signals(self, signal_id: str) -> List[PrimitiveSignal]:
        """
        Returns a list of PrimitiveSignals by their ID (e.g. 'STRONG_TREND').
        Returns an empty list if none are found.
        """
        return self._index.get(signal_id, [])

    def get_all_signals(self) -> Tuple[PrimitiveSignal, ...]:
        return self._signals
