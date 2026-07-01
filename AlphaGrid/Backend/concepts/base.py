"""Concept domain objects (Phase 8)."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any


@dataclass(frozen=True)
class Concept:
    """
    Immutable semantic event representing a market concept (e.g., 'Momentum Exhaustion').
    Once generated, it is never recalculated or mutated.
    """
    id: str
    version: str
    timestamp: datetime
    confidence: float
    inputs: Dict[str, Any]
    generator: str
