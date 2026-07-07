from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class IdentityDTO:
    id: str
    ontology_id: str
    capability_id: str
    name: str
    version: str
