from typing import Protocol, runtime_checkable, TYPE_CHECKING
from Backend.dtos.features import FeatureDTO

if TYPE_CHECKING:
    import pandas as pd

@runtime_checkable
class VolumeFeatureInterface(Protocol):
    """
    Protocol for Volume Family Features (VWAP, Relative Volume).
    """
    @property
    def component_id(self) -> str:
        ...
        
    def generate(self, data: 'pd.DataFrame', trace_id: str, correlation_id: str) -> FeatureDTO:
        ...
