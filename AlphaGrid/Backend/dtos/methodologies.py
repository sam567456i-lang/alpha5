from .base import BaseObject
from typing import Dict, Any, List

class MethodologyDTO(BaseObject):
    owner: str = "Methodology"
    is_active: bool
    direction: int
    metadata: Dict[str, Any]
