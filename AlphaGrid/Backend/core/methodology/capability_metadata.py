from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class CapabilityMetadata:
    """Explicitly versions a capability and declares its API requirements."""
    name: str
    capability_version: int
    requires_api_versions: List[str] = field(default_factory=list) # e.g. ["Evidence API v3", "Policy API v5"]
    supports_api_versions: List[str] = field(default_factory=list)
