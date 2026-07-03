from .base import BaseObject
from typing import Dict, Any
from pydantic import Field

class FeatureDTO(BaseObject):
    owner: str = "Feature"
    symbol: str
    timeframe: str
    values: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)
