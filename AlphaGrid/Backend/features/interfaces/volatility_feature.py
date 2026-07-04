from typing import Protocol, runtime_checkable, TYPE_CHECKING
from Backend.dtos.features import FeatureDTO

if TYPE_CHECKING:
    import pandas as pd

@runtime_checkable
class VolatilityFeatureInterface(Protocol):
    """
    Interface for all Volatility feature generators (ATR, Bollinger, etc).
    """
    
    @property
    def component_id(self) -> str:
        """Returns the unique component ID of the generator."""
        ...
        
    def generate(self, data: 'pd.DataFrame', trace_id: str, correlation_id: str) -> FeatureDTO:
        """
        Executes the feature generation logic.
        """
        ...
