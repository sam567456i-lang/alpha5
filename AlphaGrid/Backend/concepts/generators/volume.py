"""Volume Concept Generator."""

from typing import Any, Dict, List
from datetime import datetime
from Shared.enums.concept_state import VolumeState
from Backend.concepts.base import Concept
from Backend.concepts.generator import AbstractConceptGenerator
from Shared.enums.concept_type import ConceptType

class VolumeConceptGenerator(AbstractConceptGenerator):
    """
    Generates a 'VolumeState' Concept based on Relative Volume (RVOL).
    """

    def __init__(self, source: str = "RVOL_14") -> None:
        self.source = source
        self.surge_threshold = 2.0
        self.climax_threshold = 4.0

    def get_id(self) -> str:
        return "VolumeState"

    def get_version(self) -> str:
        return "v1"

    def get_required_features(self) -> List[str]:
        return [self.source]

    def evaluate(self, timestamp: datetime, feature_values: Dict[str, Any], geometry_cache: Any = None) -> Concept:
        rvol_data = feature_values.get(self.source, {})
        rvol = rvol_data.get("rvol", 1.0)
        
        state = VolumeState.NORMAL
        confidence = 0.5
        
        if rvol >= self.climax_threshold:
            state = VolumeState.CLIMAX
            confidence = 0.95
        elif rvol >= self.surge_threshold:
            state = VolumeState.SURGE
            confidence = 0.8
        elif rvol < 0.5:
            state = VolumeState.NORMAL # Extremely low volume
            confidence = 0.6
            
        return Concept(
            id=self.get_id(),
            type=ConceptType.VOLUME,
            version=self.get_version(),
            timestamp=timestamp,
            confidence=confidence,
            inputs={"source": self.source, "rvol": rvol, "state": state},
            generator=self.__class__.__name__
        )
