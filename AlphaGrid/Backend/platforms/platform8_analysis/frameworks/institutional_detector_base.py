from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
from Backend.platforms.platform8_analysis.frameworks.detector_base import DetectorBase

class InstitutionalZoneDetectorBase(DetectorBase):
    """
    Base class for Institutional Zones (Order Blocks, Mitigation Blocks, Breaker Blocks).
    """
    
    @abstractmethod
    def validate_zone_context(self, inputs: Dict[str, Any]) -> bool:
        pass
