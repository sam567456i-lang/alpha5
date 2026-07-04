"""Stage 0 Golden Pipeline: Canonical Validation Strategy."""

from typing import Dict, Any, List
from datetime import timedelta

from Backend.research.engine.strategy_interface import STRATEGY_REGISTRY
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.reference.legacy.features.trend import EMAFeature
from Backend.concepts.base import Concept
from Shared.enums.concept_type import ConceptType
from Backend.concepts.generator import AbstractConceptGenerator
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator, PrimitiveSignal
from Backend.methodology.base import AbstractMethodology
from Backend.methodology.evaluation import MethodologyEvaluation
from Shared.enums.signal_direction import SignalDirection

class EMA10Feature(EMAFeature):
    def __init__(self) -> None:
        super().__init__(10)
    @classmethod
    def get_name(cls) -> str: return "EMA_10"

from Backend.concepts.generators.trend import TrendConceptGenerator
from Backend.signals.primitive.generators.crossover import EMACrossoverPrimitiveSignalGenerator
from Backend.methodology.trend_following import TrendFollowingMethodology

class EMA20Feature(EMAFeature):
    def __init__(self) -> None:
        super().__init__(20)
    @classmethod
    def get_name(cls) -> str: return "EMA_20"

class CanonicalValidationConfig:
    features = [EMA10Feature, EMA20Feature]
    concept_generators = [
        TrendConceptGenerator("EMA_10"),
        TrendConceptGenerator("EMA_20")
    ]
    primitive_signal_generators = [
        EMACrossoverPrimitiveSignalGenerator("EMA_10", "EMA_20")
    ]
    methodologies = [TrendFollowingMethodology()]


class CanonicalValidationStrategy(BaseResearchStrategy):
    """
    A canonical Golden Strategy whose only purpose is to exercise the entire pipeline.
    Implements simple EMA crossover purely for structural verification.
    """
    
    @classmethod
    def get_parameter_schema(cls) -> Dict[str, Dict[str, Any]]:
        return {"confidence_threshold": {"type": float, "required": False, "default": 0.5}}

    @classmethod
    def max_label_horizon(cls) -> timedelta:
        return timedelta(0)

    def __init__(self, parameters: Dict[str, Any], random_generator: Any = None) -> None:
        super().__init__(parameters, random_generator, config=CanonicalValidationConfig)

STRATEGY_REGISTRY.register("CANONICAL_VALIDATION", CanonicalValidationStrategy)
