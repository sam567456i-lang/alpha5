"""Volume B: RSI Reversion Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.mean_reversion import MeanReversionMethodology
from Backend.features.momentum import RSIFeature
from Backend.concepts.generators.extremum import ExtremumConceptGenerator, ThresholdConfig
from Backend.signals.primitive.generators.extremum import OverextendedSignalGenerator

RSI_REVERSION = StrategyDefinition(
    id="STRAT-RSI-001",
    research_hypothesis_id="HYP-RSI-001",
    strategy_class=BaseResearchStrategy,
    methodology=MeanReversionMethodology,
    features=[RSIFeature],
    concepts=[
        ConceptDefinition(
            generator_type=ExtremumConceptGenerator,
            source="RSI_14",
            kwargs={"config": ThresholdConfig(upper=70.0, lower=30.0, high_is_bullish=False)}
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(generator_type=OverextendedSignalGenerator)
    ],
    parameters={
        "period": 14,
        "upper": 70,
        "lower": 30,
    }
)
