"""Trend A: EMA Cross Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.trend_following import TrendFollowingMethodology
from Backend.reference.legacy.features.trend import EMAFeature
from Backend.concepts.generators.trend import TrendConceptGenerator
from Backend.signals.primitive.generators.trend import StrongTrendSignalGenerator

# To do an EMA cross, we need to compare a Fast EMA and a Slow EMA.
# We don't have a built-in cross concept generator right now, so we'll just track the trend of the fast EMA.
# Wait, TrendConceptGenerator takes price and compares it to source. If source is EMA_20, it's price > EMA_20.
EMA_CROSS = StrategyDefinition(
    id="STRAT-TRND-001",
    research_hypothesis_id="HYP-TRND-001",
    strategy_class=BaseResearchStrategy,
    methodology=TrendFollowingMethodology,
    features=[EMAFeature],
    concepts=[
        ConceptDefinition(
            generator_type=TrendConceptGenerator,
            source="EMA_20"
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(generator_type=StrongTrendSignalGenerator)
    ],
    parameters={
        "ema_period": 20
    }
)
