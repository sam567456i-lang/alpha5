"""Strength Concept Generator."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
from Backend.concepts.base import Concept
from Backend.concepts.generator import AbstractConceptGenerator
from Shared.enums.concept_state import StrengthState
from Shared.enums.concept_type import ConceptType

@dataclass
class StrengthThresholdConfig:
    """Configuration for Strength thresholds."""
    weak: float = 20.0
    moderate: float = 25.0
    strong: float = 40.0

class StrengthConceptGenerator(AbstractConceptGenerator):
    """
    Generates a 'StrengthState' Concept.
    Evaluates trend strength using generic thresholds (e.g., for ADX).
    """

    def __init__(self, source: str, config: StrengthThresholdConfig, field: Optional[str] = None) -> None:
        """
        Args:
            source: The feature name (e.g., 'ADX_14')
            config: The threshold configuration.
            field: Optional sub-field (e.g., 'adx'). If None, reads the raw feature output.
        """
        self.source = source
        self.config = config
        self.field = field

    def get_id(self) -> str:
        return "StrengthState"

    def get_version(self) -> str:
        return "v1"

    def get_required_features(self) -> List[str]:
        return [self.source]

    def evaluate(self, timestamp: datetime, feature_values: Dict[str, Any], geometry_cache: Any = None) -> Concept:
        feat = feature_values[self.source]
        val = float(feat[self.field]) if self.field and isinstance(feat, dict) else float(feat)
        
        state = StrengthState.UNKNOWN
        confidence = 0.5
        
        if val >= self.config.strong:
            state = StrengthState.STRONG
            confidence = min(1.0, 0.7 + ((val - self.config.strong) / self.config.strong) * 0.3)
        elif val >= self.config.moderate:
            state = StrengthState.MODERATE
            confidence = 0.6
        elif val >= self.config.weak:
            state = StrengthState.WEAK
            confidence = 0.5
        else:
            state = StrengthState.UNKNOWN
            confidence = 0.0

        return Concept(
            id=self.get_id(),
            type=ConceptType.STRENGTH,
            version=self.get_version(),
            timestamp=timestamp,
            confidence=confidence,
            inputs={"source": self.source, "value": val, "state": state, "thresholds": {"strong": self.config.strong, "moderate": self.config.moderate, "weak": self.config.weak}},
            generator=self.__class__.__name__
        )
