"""Volatility Expansion Declarative Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.volatility import VolatilityMethodology
from Backend.features.bollinger import BollingerBandsFeature, BollingerMetricsFeature
from Backend.features.macd import MACDHistogramFeature, MACDSignalFeature, MACDLineFeature, EMA12Feature, EMA26Feature
from Backend.concepts.generators.volatility import VolatilityConceptGenerator
from Backend.concepts.generators.momentum import MomentumConceptGenerator
from Backend.signals.primitive.generators.volatility import VolatilityExpansionSignalGenerator
from Backend.signals.primitive.generators.momentum import MomentumSignalGenerator

VOLATILITY_EXPANSION = StrategyDefinition(
    id="STRAT-VOLA-001",
    research_hypothesis_id="HYP-VOLA-001",
    strategy_class=BaseResearchStrategy,
    methodology=VolatilityMethodology,
    features=[BollingerBandsFeature, BollingerMetricsFeature, MACDHistogramFeature, MACDSignalFeature, MACDLineFeature, EMA12Feature, EMA26Feature],
    concepts=[
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
        PrimitiveSignalDefinition(generator_type=VolatilityExpansionSignalGenerator),
        PrimitiveSignalDefinition(generator_type=MomentumSignalGenerator)
    ],
    parameters={
        "bollinger_period": 20,
        "macd_fast": 12,
        "macd_slow": 26,
        "macd_signal": 9
    }
)
