from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
from Backend.platforms.platform8_analysis.frameworks.detector_base import DetectorBase

class AuctionDetectorBase(DetectorBase):
    """
    Base class for Auction Market Theory (AMT) Detectors (POC, Value Areas, Profile Shapes).
    """
    
    @abstractmethod
    def validate_auction_context(self, inputs: Dict[str, Any]) -> bool:
        pass
