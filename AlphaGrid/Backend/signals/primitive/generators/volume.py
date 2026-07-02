"""Volume Primitive Signal Generators."""

from datetime import datetime
from typing import List, Optional
from Backend.concepts.base import Concept
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator, PrimitiveSignal
from Shared.enums.concept_type import ConceptType
from Shared.enums.concept_state import VolumeState

class VolumeSurgeSignalGenerator(AbstractPrimitiveSignalGenerator):
    """
    Generates a VOLUME_SURGE signal if Volume Concept detects a SURGE or CLIMAX.
    """

    @classmethod
    def get_id(cls) -> str:
        return "VOLUME_SURGE"

    @classmethod
    def get_required_concepts(cls) -> List[ConceptType]:
        return [ConceptType.VOLUME]

    def evaluate(self, timestamp: datetime, concepts: List[Concept]) -> Optional[PrimitiveSignal]:
        volumes = [c for c in concepts if c.type == ConceptType.VOLUME]
        
        if not volumes:
            return None
            
        volume = volumes[0]
        state = volume.inputs.get("state", VolumeState.UNKNOWN)
        
        if state in [VolumeState.SURGE, VolumeState.CLIMAX]:
            return PrimitiveSignal(
                id=self.get_id(),
                timestamp=timestamp,
                direction=0, # Volume alone does not have direction
                confidence=volume.confidence,
                supporting_concepts=(volume.id,),
                generator=self.get_id()
            )
            
        return None
