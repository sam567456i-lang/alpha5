from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
from Backend.platforms.platform8_analysis.frameworks.detector_base import DetectorBase

class ImbalanceDetectorBase(DetectorBase):
    """
    Base class for Imbalance Detectors (FVG, BISI, SIBI).
    """
    
    @abstractmethod
    def validate_imbalance_context(self, inputs: Dict[str, Any]) -> bool:
        pass
