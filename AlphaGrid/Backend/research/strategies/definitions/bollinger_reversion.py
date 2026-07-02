"""Volume B: Bollinger Reversion Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.mean_reversion import MeanReversionMethodology
from Backend.features.bollinger import BollingerBandsFeature, BollingerMetricsFeature
from Backend.concepts.generators.extremum import ExtremumConceptGenerator, ThresholdConfig
from Backend.concepts.generators.volatility import VolatilityConceptGenerator
from Backend.signals.primitive.generators.extremum import OverextendedSignalGenerator

BOLLINGER_REVERSION = StrategyDefinition(
    id="STRAT-BLL-001",
    research_hypothesis_id="HYP-BLL-001",
    strategy_class=BaseResearchStrategy,
    methodology=MeanReversionMethodology,
    features=[BollingerBandsFeature, BollingerMetricsFeature],
    concepts=[
        ConceptDefinition(
            generator_type=ExtremumConceptGenerator,
            source="Bollinger_Metrics",
            kwargs={"field": "z_score", "config": ThresholdConfig(upper=2.0, lower=-2.0, high_is_bullish=False)}
        ),
        ConceptDefinition(
            generator_type=VolatilityConceptGenerator,
            source="Bollinger_Metrics",
            kwargs={"field": "band_width"}
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(generator_type=OverextendedSignalGenerator)
    ],
    parameters={
        "period": 20,
        "std_dev": 2.0
    }
)
