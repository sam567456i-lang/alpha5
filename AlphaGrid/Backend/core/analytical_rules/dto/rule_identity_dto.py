from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class RuleIdentityDTO:
    """Uniquely identifies an analytical rule version and execution context."""
    id: str
    version: str
    registry_checksum: str
    producer_rule: str
    ontology_id: Optional[str] = None
    capability_id: Optional[str] = None
