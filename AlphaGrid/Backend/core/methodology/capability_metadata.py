from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass(frozen=True)
class CapabilityMetadata:
    """Explicitly versions a capability and declares its API requirements."""
    id: str
    name: str
    version: str
    owner: str
    dependencies: List[str] = field(default_factory=list)
    required_features: List[str] = field(default_factory=list)
    required_data: List[str] = field(default_factory=list)
    required_capabilities: List[str] = field(default_factory=list)
    output_types: List[str] = field(default_factory=list)
    priority: int = 0
    parallelizable: bool = False
    deterministic: bool = True
    streaming_supported: bool = False
    replay_supported: bool = True

