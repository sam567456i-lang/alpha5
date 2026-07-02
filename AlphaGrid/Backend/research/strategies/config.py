"""Strategy Configuration."""

from dataclasses import dataclass
from typing import List, Type
from Backend.features.base import AbstractFeature
from Backend.concepts.generator import AbstractConceptGenerator
from Backend.methodology.base import AbstractMethodology
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator

@dataclass
class StrategyConfig:
    """
    Declarative configuration for a Research Strategy pipeline.
    Replaces 1:1 strategy classes by allowing the framework to perform dependency injection.
    """
    features: List[Type[AbstractFeature]]
    concept_generators: List[AbstractConceptGenerator]
    primitive_signal_generators: List[AbstractPrimitiveSignalGenerator]
    methodologies: List[AbstractMethodology]
