"""Abstract Strategy Base Class and Parameter Search Governance."""

from typing import Dict, Any, List
from datetime import datetime
from abc import ABC, abstractmethod
from Backend.strategy.objects import TradingDecision

class ParameterSearchProtocol:
    """Defines the stages of parameter search governance."""
    STAGE_1_DEFAULT = "DEFAULT_PARAMETERS"
    STAGE_2_GRID = "SMALL_GRID_SEARCH"
    STAGE_3_BAYESIAN = "BAYESIAN_OPTIMIZATION"
    STAGE_4_WALKFORWARD = "WALKFORWARD_VALIDATION"
    STAGE_5_MONTECARLO = "MONTECARLO_ROBUSTNESS"

class AbstractStrategy(ABC):
    """
    Abstract Strategy Base Class.
    Enforces STRATEGY_METADATA and Parameter Search Governance.
    """
    
    @property
    @abstractmethod
    def STRATEGY_METADATA(self) -> Dict[str, Any]:
        """Must return strategy metadata."""
        pass

    def __init__(self, parameters: Dict[str, Any] = None):
        self.parameters = parameters or {}
        
    @abstractmethod
    def evaluate(self, timestamp: datetime, methodologies: List[Any]) -> List[TradingDecision]:
        """Evaluates methodologies to generate Trading Decisions."""
        pass
        
    @classmethod
    def get_parameter_search_protocol(cls) -> Dict[str, Any]:
        """
        Returns the mandatory parameter search protocol for this strategy.
        This enforces governance on how strategy parameters are optimized.
        """
        return {
            "stages": [
                ParameterSearchProtocol.STAGE_1_DEFAULT,
                ParameterSearchProtocol.STAGE_2_GRID,
                ParameterSearchProtocol.STAGE_3_BAYESIAN,
                ParameterSearchProtocol.STAGE_4_WALKFORWARD,
                ParameterSearchProtocol.STAGE_5_MONTECARLO
            ],
            "default_parameters": cls._get_default_parameters(),
            "grid_search_space": cls._get_grid_search_space()
        }
        
    @classmethod
    def _get_default_parameters(cls) -> Dict[str, Any]:
        """Returns the Stage 1 default parameters."""
        return {}
        
    @classmethod
    def _get_grid_search_space(cls) -> Dict[str, List[Any]]:
        """Returns the Stage 2 small grid search space."""
        return {}
