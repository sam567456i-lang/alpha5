from typing import Protocol, runtime_checkable, TYPE_CHECKING
from Backend.dtos.features import FeatureDTO

if TYPE_CHECKING:
    import pandas as pd

@runtime_checkable
class ExtremumFeatureInterface(Protocol):
    """
    Protocol for Extremum Family Features.
    Generators implementing this must output FeatureDTO representing structural 
    extremes (highs, lows, support, resistance) without embedding semantic 
    logic like 'breakout=True' (which belongs in the Concept layer).
    """
    def generate(self, data: 'pd.DataFrame', trace_id: str, correlation_id: str) -> FeatureDTO:
        ...
