from __future__ import annotations
from typing import Protocol, runtime_checkable, TYPE_CHECKING
if TYPE_CHECKING:
    import pandas as pd
from Backend.dtos.features import FeatureDTO

@runtime_checkable
class MomentumFeatureInterface(Protocol):
    """
    Standardizes the outputs for any momentum-based indicator
    ensuring they all produce compatible semantics for the concept layer.
    """
    
    @property
    def component_id(self) -> str:
        ...
        
    def generate(self, data: pd.DataFrame, trace_id: str, correlation_id: str) -> FeatureDTO:
        """
        Must return a FeatureDTO containing numerical indicator outputs.
        """
        ...
