"""Mean Reversion D: Keltner Reversion Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.mean_reversion import MeanReversionMethodology
from Backend.features.keltner import KeltnerChannelFeature
from Backend.reference.legacy.features.trend import EMAFeature
from Backend.features.volatility import ATRFeature
from Backend.concepts.generators.extremum import ExtremumConceptGenerator, ThresholdConfig
from Backend.signals.primitive.generators.extremum import OverextendedSignalGenerator

# Note: Keltner channels output a dict with upper_band, lower_band, ema.
# We will use ExtremumConceptGenerator on a placeholder distance metric if KeltnerMetrics were added.
# For now we'll register the base Keltner channel for structural completeness.
KELTNER_REVERSION = StrategyDefinition(
    id="STRAT-REV-004",
    research_hypothesis_id="HYP-REV-004",
    strategy_class=BaseResearchStrategy,
    methodology=MeanReversionMethodology,
    features=[KeltnerChannelFeature, EMAFeature, ATRFeature],
    concepts=[
        ConceptDefinition(
            generator_type=ExtremumConceptGenerator,
            source="Keltner_20_2",
            kwargs={
                "field": "upper_band", # Proxying a field just to validate execution
                "config": ThresholdConfig(upper=99999.0, lower=-99999.0)
            }
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(generator_type=OverextendedSignalGenerator)
    ],
    parameters={
        "period": 20,
        "multiplier": 2.0
    }
)
