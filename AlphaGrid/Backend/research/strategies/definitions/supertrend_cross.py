"""Volume A: SuperTrend Cross Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.trend_following import TrendFollowingMethodology
from Backend.features.supertrend import SuperTrendFeature
from Backend.features.adx import ADXFeature

from Backend.concepts.generators.trend import TrendConceptGenerator
from Backend.concepts.generators.strength import StrengthConceptGenerator, StrengthThresholdConfig
from Backend.signals.primitive.generators.trend import StrongTrendSignalGenerator

SUPERTREND_CROSS = StrategyDefinition(
    id="STRAT-ST-001",
    research_hypothesis_id="HYP-ST-001",
    strategy_class=BaseResearchStrategy,
    methodology=TrendFollowingMethodology,
    features=[SuperTrendFeature, ADXFeature],
    concepts=[
        ConceptDefinition(
            generator_type=TrendConceptGenerator,
            source="SuperTrend_10_3"
        ),
        ConceptDefinition(
            generator_type=StrengthConceptGenerator,
            source="ADX_14",
            kwargs={"field": "adx", "config": StrengthThresholdConfig(weak=20.0, moderate=25.0, strong=30.0)}
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(generator_type=StrongTrendSignalGenerator)
    ],
    parameters={
        "supertrend_period": 10,
        "supertrend_multiplier": 3.0,
        "adx_period": 14
    }
)
