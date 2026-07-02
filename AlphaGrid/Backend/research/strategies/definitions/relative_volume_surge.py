"""Relative Volume Surge Declarative Strategy Definition."""

from Backend.research.strategies.definition import StrategyDefinition, ConceptDefinition, PrimitiveSignalDefinition
from Backend.research.strategies.base_research_strategy import BaseResearchStrategy
from Backend.methodology.volume_analysis import VolumeAnalysisMethodology
from Backend.features.relative_volume import RelativeVolumeFeature
from Backend.features.macd import MACDHistogramFeature, MACDSignalFeature, MACDLineFeature, EMA12Feature, EMA26Feature
from Backend.concepts.generators.volume import VolumeConceptGenerator
from Backend.concepts.generators.momentum import MomentumConceptGenerator
from Backend.signals.primitive.generators.volume import VolumeSurgeSignalGenerator
from Backend.signals.primitive.generators.momentum import MomentumSignalGenerator

RELATIVE_VOLUME_SURGE = StrategyDefinition(
    id="STRAT-VOL-001",
    research_hypothesis_id="HYP-VOL-001",
    strategy_class=BaseResearchStrategy,
    methodology=VolumeAnalysisMethodology,
    features=[RelativeVolumeFeature, MACDHistogramFeature, MACDSignalFeature, MACDLineFeature, EMA12Feature, EMA26Feature],
    concepts=[
        ConceptDefinition(
            generator_type=VolumeConceptGenerator,
            source="RVOL_14"
        ),
        ConceptDefinition(
            generator_type=MomentumConceptGenerator,
            source="MACD_Histogram"
        )
    ],
    primitive_signals=[
        PrimitiveSignalDefinition(generator_type=VolumeSurgeSignalGenerator),
        PrimitiveSignalDefinition(generator_type=MomentumSignalGenerator)
    ],
    parameters={
        "rvol_period": 14,
        "macd_fast": 12,
        "macd_slow": 26,
        "macd_signal": 9
    }
)
