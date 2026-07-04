"""Trend D: Donchian Trend Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.trend_following import TrendFollowingMethodology
from Backend.reference.legacy.features.donchian import Donchian20Feature
from Backend.concepts.generators.trend import TrendConceptGenerator
from Backend.signals.primitive.generators.trend import StrongTrendSignalGenerator

DONCHIAN_TREND = StrategyDefinition(
    id="STRAT-TRND-004",
    research_hypothesis_id="HYP-TRND-004",
    strategy_class=BaseResearchStrategy,
    methodology=TrendFollowingMethodology,
    features=[Donchian20Feature],
    concepts=[
        ConceptDefinition(
            generator_type=TrendConceptGenerator,
            source="Donchian_20",
            kwargs={"price_field": "close"}
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(generator_type=StrongTrendSignalGenerator)
    ],
    parameters={
        "period": 20
    }
)
