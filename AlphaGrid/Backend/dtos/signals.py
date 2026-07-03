from .base import BaseObject
from typing import Dict, Any
from pydantic import Field

class SignalDTO(BaseObject):
    owner: str = "Signal"
    direction: int
    signal_type: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
