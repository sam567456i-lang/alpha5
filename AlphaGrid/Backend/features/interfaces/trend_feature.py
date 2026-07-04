from typing import Protocol, runtime_checkable, TYPE_CHECKING
from Backend.dtos.features import FeatureDTO

if TYPE_CHECKING:
    import pandas as pd

@runtime_checkable
class TrendFeatureInterface(Protocol):
    """
    Interface for all Trend feature generators (EMA, SMA, etc).
    All Trend features must adhere to this protocol for the pipeline to accept them.
    """
    
    @property
    def component_id(self) -> str:
        """Returns the unique component ID of the generator."""
        ...
        
    def generate(self, data: 'pd.DataFrame', trace_id: str, correlation_id: str) -> FeatureDTO:
        """
        Executes the feature generation logic.
        
        Args:
            data: Market data dataframe.
            trace_id: Execution trace ID.
            correlation_id: Request correlation ID.
            
        Returns:
            A constructed FeatureDTO.
        """
        ...
