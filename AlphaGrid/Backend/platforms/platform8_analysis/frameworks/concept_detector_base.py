from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
from Backend.platforms.platform8_analysis.frameworks.detector_base import DetectorBase

class ConceptDetectorBase(DetectorBase):
    """
    Intermediate base class for all Concept-level Detectors (Liquidity, Structure, etc.).
    Handles common concept-generation logic to avoid duplication across concept families.
    """
    
    @abstractmethod
    def validate_concept_context(self, inputs: Dict[str, Any]) -> bool:
        """
        Validates that required feature-level context is present before concept generation.
        """
        pass
