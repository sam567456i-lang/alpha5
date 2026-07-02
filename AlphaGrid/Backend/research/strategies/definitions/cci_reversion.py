"""Mean Reversion E: CCI Reversion Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.mean_reversion import MeanReversionMethodology
from Backend.features.cci import CCIFeature
from Backend.concepts.generators.extremum import ExtremumConceptGenerator, ThresholdConfig
from Backend.signals.primitive.generators.extremum import OverextendedSignalGenerator

CCI_REVERSION = StrategyDefinition(
    id="STRAT-REV-005",
    research_hypothesis_id="HYP-REV-005",
    strategy_class=BaseResearchStrategy,
    methodology=MeanReversionMethodology,
    features=[CCIFeature],
    concepts=[
        ConceptDefinition(
            generator_type=ExtremumConceptGenerator,
            source="CCI_20",
            kwargs={
                "config": ThresholdConfig(upper=100.0, lower=-100.0, high_is_bullish=True)
            }
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(generator_type=OverextendedSignalGenerator)
    ],
    parameters={
        "period": 20,
        "overbought": 100.0,
        "oversold": -100.0
    }
)
