"""Momentum B: ROC Momentum Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.momentum import MomentumMethodology
from Backend.features.momentum import ROCFeature
from Backend.concepts.generators.momentum import MomentumConceptGenerator
from Backend.signals.primitive.generators.momentum import MomentumSignalGenerator

ROC_MOMENTUM = StrategyDefinition(
    id="STRAT-MOM-002",
    research_hypothesis_id="HYP-MOM-002",
    strategy_class=BaseResearchStrategy,
    methodology=MomentumMethodology,
    features=[ROCFeature],
    concepts=[
        ConceptDefinition(
            generator_type=MomentumConceptGenerator,
            source="ROC_5"
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(generator_type=MomentumSignalGenerator)
    ],
    parameters={
        "roc_period": 14
    }
)
