"""Mean Reversion C: Stochastic Reversion Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.mean_reversion import MeanReversionMethodology
from Backend.features.stochastic import StochasticFeature
from Backend.concepts.generators.extremum import ExtremumConceptGenerator, ThresholdConfig
from Backend.signals.primitive.generators.extremum import OverextendedSignalGenerator

STOCHASTIC_REVERSION = StrategyDefinition(
    id="STRAT-REV-003",
    research_hypothesis_id="HYP-REV-003",
    strategy_class=BaseResearchStrategy,
    methodology=MeanReversionMethodology,
    features=[StochasticFeature],
    concepts=[
        ConceptDefinition(
            generator_type=ExtremumConceptGenerator,
            source="Stochastic_14_3",
            kwargs={
                "field": "k",
                "config": ThresholdConfig(upper=80.0, lower=20.0, high_is_bullish=True)
            }
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(generator_type=OverextendedSignalGenerator)
    ],
    parameters={
        "k_period": 14,
        "d_period": 3,
        "overbought": 80.0,
        "oversold": 20.0
    }
)
