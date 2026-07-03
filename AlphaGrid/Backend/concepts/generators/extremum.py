"""Extremum Concept Generator."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
from Backend.concepts.base import Concept
from Backend.concepts.generator import AbstractConceptGenerator
from Shared.enums.concept_state import ExtremumState
from Shared.enums.concept_type import ConceptType

@dataclass
class ThresholdConfig:
    """Configuration for Extremum thresholds."""
    upper: float
    lower: float
    # If True, high values are overbought/bullish. 
    # If False, high values are oversold/bearish.
    high_is_bullish: bool = True

class ExtremumConceptGenerator(AbstractConceptGenerator):
    """
    Generates an 'ExtremumState' Concept.
    Evaluates overbought/oversold conditions using generic thresholds.
    """

    def __init__(self, source: str, config: ThresholdConfig, field: Optional[str] = None) -> None:
        """
        Args:
            source: The feature name (e.g., 'Bollinger_Metrics' or 'RSI_14')
            config: The threshold configuration.
            field: Optional sub-field (e.g., 'z_score'). If None, reads the raw feature output.
        """
        self.source = source
        self.config = config
        self.field = field

    def get_id(self) -> str:
        if self.field:
            return f"ExtremumState_{self.source}_{self.field}"
        return f"ExtremumState_{self.source}"

    def get_version(self) -> str:
        return "v2"

    def get_required_features(self) -> List[str]:
        return [self.source]

    def evaluate(self, timestamp: datetime, feature_values: Dict[str, Any], geometry_cache: Any = None) -> Concept:
        feat = feature_values[self.source]
        val = float(feat[self.field]) if self.field and isinstance(feat, dict) else float(feat)
        
        state = ExtremumState.NEUTRAL
        confidence = 0.5
        
        if val >= self.config.upper:
            state = ExtremumState.OVEREXTENDED_BULLISH if self.config.high_is_bullish else ExtremumState.OVEREXTENDED_BEARISH
            divisor = self.config.upper if self.config.upper != 0 else 1.0
            confidence = min(1.0, 0.5 + ((val - self.config.upper) / abs(divisor)) * 0.5)
        elif val <= self.config.lower:
            state = ExtremumState.OVEREXTENDED_BEARISH if self.config.high_is_bullish else ExtremumState.OVEREXTENDED_BULLISH
            divisor = self.config.lower if self.config.lower != 0 else 1.0
            confidence = min(1.0, 0.5 + ((self.config.lower - val) / abs(divisor)) * 0.5)

        return Concept(
            id=self.get_id(),
            type=ConceptType.EXTREMUM,
            version=self.get_version(),
            timestamp=timestamp,
            confidence=confidence,
            inputs={"source": self.source, "value": val, "state": state, "thresholds": {"upper": self.config.upper, "lower": self.config.lower}},
            generator=self.__class__.__name__
        )
