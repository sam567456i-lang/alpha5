from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple
from Backend.Platform10.contracts.dtos import MarketStateDTO, ConfidenceFactorsDTO

class IMethodologyPlugin(ABC):
    """Base interface for all Platform 10 Methodologies"""
    
    @property
    @abstractmethod
    def methodology_id(self) -> str:
        """Returns the unique Registry ID of this methodology"""
        pass
        
    @property
    @abstractmethod
    def version(self) -> str:
        pass
        
    @property
    @abstractmethod
    def capability_family(self) -> str:
        """e.g. 'trend', 'momentum', 'mean_reversion'"""
        pass

    @abstractmethod
    def evaluate_factors(self, market_state: MarketStateDTO) -> Tuple[ConfidenceFactorsDTO, Dict[str, Any]]:
        """
        Executes the methodology against the provided market state.
        Returns:
            - ConfidenceFactorsDTO: The multi-dimensional confidence factors (e.g. Trend=0.8, Momentum=0.7)
            - raw_data (Dict): Raw internal calculations to be consumed by Evidence and Explainability Builders.
        """
        pass
