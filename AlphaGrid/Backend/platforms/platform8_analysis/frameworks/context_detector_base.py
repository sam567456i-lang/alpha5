from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
from Backend.platforms.platform8_analysis.frameworks.detector_base import DetectorBase

class ContextDetectorBase(DetectorBase):
    """
    Base class for Context Detectors (Timeframes, Sessions, Regimes).
    """
    
    @abstractmethod
    def validate_environment_context(self, inputs: Dict[str, Any]) -> bool:
        pass
