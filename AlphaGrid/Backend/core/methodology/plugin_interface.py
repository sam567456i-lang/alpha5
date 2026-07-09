from abc import ABC, abstractmethod
from typing import Dict, Any

from Backend.core.methodology.multi_timeframe_graph import MultiTimeframeEvidenceGraph
from Backend.core.methodology.narrative_graph import NarrativeGraph
from Backend.core.methodology.narrative_types import MethodologyType

class MethodologyPlugin(ABC):
    """
    Abstract base class for Platform 11 Methodology Plugins (e.g. ICT, SMC).
    Consumes multi-timeframe objective evidence to emit subjective narratives.
    MUST NOT compute geometric properties; only interprets them.
    """
    
    @property
    @abstractmethod
    def methodology_type(self) -> MethodologyType:
        """Returns the specific methodology identifier (e.g., ICT, SMC)."""
        pass
        
    @property
    @abstractmethod
    def version(self) -> str:
        """Returns the version of this methodology plugin."""
        pass
        
    @abstractmethod
    def execute(self, mtf_graph: MultiTimeframeEvidenceGraph, context: Dict[str, Any] = None) -> NarrativeGraph:
        """
        Consumes the entire objective environment context across all available timeframes.
        Returns a NarrativeGraph specific to this methodology.
        """
        pass
