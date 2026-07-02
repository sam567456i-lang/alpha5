"""MACD Momentum Declarative Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.momentum import MomentumMethodology
from Backend.features.macd import MACDHistogramFeature, MACDSignalFeature, MACDLineFeature, EMA12Feature, EMA26Feature
from Backend.concepts.generators.momentum import MomentumConceptGenerator
from Backend.signals.primitive.generators.momentum import MomentumSignalGenerator

MACD_MOMENTUM = StrategyDefinition(
    id="STRAT-MOM-001",
    research_hypothesis_id="HYP-MOM-001",
    strategy_class=BaseResearchStrategy,
    methodology=MomentumMethodology,
    features=[MACDHistogramFeature, MACDSignalFeature, MACDLineFeature, EMA12Feature, EMA26Feature],
    concepts=[
        ConceptDefinition(
            generator_type=MomentumConceptGenerator,
            source="MACD_Histogram"
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(
            generator_type=MomentumSignalGenerator
        )
    ],
    parameters={
        "fast_period": 12,
        "slow_period": 26,
        "signal_period": 9
    }
)
