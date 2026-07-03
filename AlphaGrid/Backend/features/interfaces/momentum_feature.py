from typing import Protocol, runtime_checkable
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
        Must return a FeatureDTO where the `values` dict contains:
        - momentum_strength (float): Magnitude of the momentum
        - momentum_direction (float): 1.0 (Up), -1.0 (Down)
        - momentum_acceleration (float): Rate of change of momentum (optional, 0.0 if not supported)
        """
        ...
