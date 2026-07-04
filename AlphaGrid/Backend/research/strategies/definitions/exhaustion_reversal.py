"""Exhaustion Reversal Declarative Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.reversal import ReversalMethodology
from Backend.reference.legacy.features.momentum import RSIFeature
from Backend.features.bollinger import BollingerBandsFeature
from Backend.reference.legacy.features.volatility import ATRFeature
from Backend.concepts.generators.extremum import ExtremumConceptGenerator, ThresholdConfig
from Backend.concepts.generators.volatility import VolatilityConceptGenerator
from Backend.concepts.generators.momentum import MomentumConceptGenerator
from Backend.signals.primitive.generators.extremum import OverextendedSignalGenerator
from Backend.signals.primitive.generators.momentum import MomentumExhaustionSignalGenerator

EXHAUSTION_REVERSAL = StrategyDefinition(
    id="STRAT-REV-001",
    research_hypothesis_id="HYP-REV-001",
    strategy_class=BaseResearchStrategy,
    methodology=ReversalMethodology,
    features=[RSIFeature, BollingerBandsFeature, ATRFeature],
    concepts=[
        ConceptDefinition(
            generator_type=ExtremumConceptGenerator,
            source="RSI_14",
            kwargs={"config": ThresholdConfig(upper=75.0, lower=25.0, high_is_bullish=False)}
        ),
        ConceptDefinition(
            generator_type=VolatilityConceptGenerator,
            source="Bollinger_Metrics",
            kwargs={"field": "band_width"}
        ),
        ConceptDefinition(
            generator_type=MomentumConceptGenerator,
            source="MACD_Histogram"
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(generator_type=OverextendedSignalGenerator),
        PrimitiveSignalDefinition(generator_type=MomentumExhaustionSignalGenerator)
    ],
    parameters={
        "rsi_period": 14,
        "bollinger_period": 20
    }
)
