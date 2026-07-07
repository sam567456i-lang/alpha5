from abc import abstractmethod
from typing import Any, Dict
from Backend.platforms.platform8_analysis.frameworks.concept_detector_base import ConceptDetectorBase

class LiquidityDetectorBase(ConceptDetectorBase):
    """
    Base class specifically for Liquidity Detectors.
    Provides built-in shared logic for tolerances, timeframes, and metadata extraction.
    """
    
    def validate_concept_context(self, inputs: Dict[str, Any]) -> bool:
        """Implements ConceptDetectorBase validation."""
        return self._validate_context(inputs)

    def _validate_context(self, inputs: Dict[str, Any]) -> bool:
        """Shared liquidity context validation."""
        return True
        
    def _apply_tolerance(self, price: float, tolerance: Dict[str, Any]) -> float:
        """Shared tolerance calculation (absolute or percentage)."""
        return price
        
    def _align_timeframes(self, timeframes: list) -> bool:
        """Shared timeframe alignment."""
        return True
        
    def _align_sessions(self, sessions: list) -> bool:
        """Shared session alignment."""
        return True
        
    def _calculate_freshness(self) -> float:
        """Shared freshness policy execution."""
        return 1.0
        
    def _calculate_confidence(self) -> float:
        """Shared confidence modeling execution."""
        return 1.0
        
    def _load_metadata_from_registry(self, capability_id: str) -> Dict[str, Any]:
        """
        Dynamically extracts configuration for the capability from the governance registry.
        """
        return {}
        
    @abstractmethod
    def validate_liquidity_context(self, inputs: Dict[str, Any]) -> bool:
        pass
