from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass(frozen=True)
class RuleMetadataDTO:
    """Metadata governing rule capabilities, timeouts, and boundaries."""
    name: str
    description: str
    owner: str
    execution_stage: int
    priority: int
    timeout_ms: int
    tags: List[str]
    capabilities: Dict[str, Any]
