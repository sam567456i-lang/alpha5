"""Primitive Signal Engine.

Executes Primitive Signal Generators against an evaluated Concept context.
"""

from typing import List, Tuple
from datetime import datetime
from Backend.concepts.base import Concept
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator, PrimitiveSignal

class PrimitiveSignalEngine:
    """
    Executes a configured list of AbstractPrimitiveSignalGenerators.
    Takes raw Concepts from Phase 8 and transforms them into atomic Primitive Signals for Methodologies.
    """

    ENGINE_METADATA = {
        "owner": "Primitive Signal Domain",
        "version": "1.0.0",
        "consumes": "Concept",
        "produces": "PrimitiveSignal",
        "registry": "primitive_signal_registry",
        "contract_version": "v1",
        "downstream": "MethodologyEngine"
    }

    def __init__(self, generators: List[AbstractPrimitiveSignalGenerator]) -> None:
        """
        Initializes the PrimitiveSignalEngine.

        Args:
            generators: An ordered list of instantiated Primitive Signal generators.
        """
        self.generators = generators

    def process(self, timestamp: datetime, concepts: List[Concept]) -> Tuple[PrimitiveSignal, ...]:
        """
        Evaluates all generators against the given concepts.

        Args:
            timestamp: The timestamp of the current evaluation.
            concepts: The concepts generated for this timestamp.

        Returns:
            A tuple of emitted PrimitiveSignals.
        """
        signals = []
        for gen in self.generators:
            # Note: A real implementation might filter concepts down to only the ones required by `gen.get_required_concepts()`
            # For simplicity, we pass all concepts and let the generator extract what it needs.
            try:
                signal = gen.evaluate(timestamp, concepts)
                if signal:
                    signals.append(signal)
            except Exception as e:
                raise RuntimeError(f"Primitive Signal Generator {gen.get_id()} failed during evaluation.") from e
                
        return tuple(signals)
