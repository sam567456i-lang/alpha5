from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class PolicyIdentity:
    """Rich identity for methodology policies ensuring deterministic replay."""
    version: str # e.g. "1.3"
    semantic_version: str # e.g. "1.3.0"
    hash: str # SHA-256 for integrity
    parent_version: str # e.g. "1.2"
    policy_family: str # e.g. "ICT_SMT"
    compatibility: str # e.g. "BACKWARD_COMPATIBLE"
    created: datetime
    author: str
