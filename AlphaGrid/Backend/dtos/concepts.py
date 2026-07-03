from .base import BaseObject
from typing import Dict, Any

class ConceptDTO(BaseObject):
    owner: str = "Concept"
    concept_type: str
    state: str
    metadata: Dict[str, Any]
