"""Trend B: SMA Cross Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.trend_following import TrendFollowingMethodology
from Backend.reference.legacy.features.trend import SMAFeature
from Backend.concepts.generators.trend import TrendConceptGenerator
from Backend.signals.primitive.generators.trend import StrongTrendSignalGenerator

SMA_CROSS = StrategyDefinition(
    id="STRAT-TRND-002",
    research_hypothesis_id="HYP-TRND-002",
    strategy_class=BaseResearchStrategy,
    methodology=TrendFollowingMethodology,
    features=[SMAFeature],
    concepts=[
        ConceptDefinition(
            generator_type=TrendConceptGenerator,
            source="SMA_20"
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(generator_type=StrongTrendSignalGenerator)
    ],
    parameters={
        "sma_period": 20
    }
)
