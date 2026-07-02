"""Momentum C: Stochastic Momentum Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.momentum import MomentumMethodology
from Backend.features.stochastic import StochasticFeature
from Backend.concepts.generators.momentum import MomentumConceptGenerator
from Backend.signals.primitive.generators.momentum import MomentumSignalGenerator

STOCHASTIC_MOMENTUM = StrategyDefinition(
    id="STRAT-MOM-003",
    research_hypothesis_id="HYP-MOM-003",
    strategy_class=BaseResearchStrategy,
    methodology=MomentumMethodology,
    features=[StochasticFeature],
    concepts=[
        ConceptDefinition(
            generator_type=MomentumConceptGenerator,
            source="Stochastic_14_3",
            kwargs={"field": "k"}
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(generator_type=MomentumSignalGenerator)
    ],
    parameters={
        "k_period": 14,
        "d_period": 3
    }
)
