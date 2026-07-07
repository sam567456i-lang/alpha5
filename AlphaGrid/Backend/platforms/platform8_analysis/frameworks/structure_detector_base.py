from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
from Backend.platforms.platform8_analysis.frameworks.detector_base import DetectorBase

class StructureDetectorBase(DetectorBase):
    """
    Base class specifically for Market Structure Detectors (CHoCH, BOS, Swings).
    Provides built-in methods for multi-timeframe alignment checks.
    """
    
    @abstractmethod
    def validate_structure_context(self, inputs: Dict[str, Any]) -> bool:
        """
        Validates that required geometry (e.g. valid swings) is present
        before executing structure detection.
        """
        pass
