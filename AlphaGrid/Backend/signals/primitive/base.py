"""Primitive Signal Framework (Layer 3)."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple, Optional
from Backend.concepts.base import Concept
from Shared.enums.concept_type import ConceptType


@dataclass(frozen=True)
class PrimitiveSignal:
    """
    Atomic, deterministic observation generated from one or more Concepts.
    Must not contain trade management, portfolio logic, or methodology logic.
    """
    id: str
    timestamp: datetime
    direction: int  # 1 (Bullish), -1 (Bearish), 0 (Neutral)
    confidence: float
    supporting_concepts: Tuple[str, ...] = field(default_factory=tuple)
    generator: str = ""


class AbstractPrimitiveSignalGenerator(ABC):
    """
    Base class for generating Primitive Signals from Concepts.
    """

    @classmethod
    @abstractmethod
    def get_id(cls) -> str:
        """Unique ID of this signal generator."""
        pass

    @classmethod
    @abstractmethod
    def get_required_concepts(cls) -> List[ConceptType]:
        """List of ConceptTypes required to generate this signal."""
        pass

    @abstractmethod
    def evaluate(self, timestamp: datetime, concepts: List[Concept]) -> Optional[PrimitiveSignal]:
        """
        Evaluates the required concepts and produces a PrimitiveSignal.
        """
        pass
