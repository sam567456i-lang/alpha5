"""Reversal B: Stochastic Exhaustion Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.reversal import ReversalMethodology
from Backend.features.stochastic import StochasticFeature
from Backend.concepts.generators.extremum import ExtremumConceptGenerator, ThresholdConfig
from Backend.concepts.generators.momentum import MomentumConceptGenerator
from Backend.signals.primitive.generators.extremum import OverextendedSignalGenerator
from Backend.signals.primitive.generators.momentum import MomentumExhaustionSignalGenerator

STOCHASTIC_EXHAUSTION = StrategyDefinition(
    id="STRAT-REVS-002",
    research_hypothesis_id="HYP-REVS-002",
    strategy_class=BaseResearchStrategy,
    methodology=ReversalMethodology,
    features=[StochasticFeature],
    concepts=[
        ConceptDefinition(
            generator_type=ExtremumConceptGenerator,
            source="Stochastic_14_3",
            kwargs={
                "field": "k",
                "config": ThresholdConfig(upper=80.0, lower=20.0, high_is_bullish=True)
            }
        ),
        ConceptDefinition(
            generator_type=MomentumConceptGenerator,
            source="Stochastic_14_3",
            kwargs={"field": "k"}
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(generator_type=OverextendedSignalGenerator),
        PrimitiveSignalDefinition(generator_type=MomentumExhaustionSignalGenerator)
    ],
    parameters={
        "k_period": 14,
        "d_period": 3,
        "overbought": 80.0,
        "oversold": 20.0
    }
)
