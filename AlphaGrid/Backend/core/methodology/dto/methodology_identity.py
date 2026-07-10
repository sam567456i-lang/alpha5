from dataclasses import dataclass, field
from typing import List, Dict, Optional
import datetime

@dataclass(frozen=True)
class MethodologyMetadata:
    id: str
    version: str
    author: str
    description: str
    supported_markets: List[str]
    required_capabilities: List[str]
    required_evidence: List[str]
    optional_evidence: List[str]
    minimum_sdk_version: str
    status: str  # e.g., Experimental, Research, Certified, Frozen, Deprecated
    certification_level: str
    compatibility: Dict[str, str]

@dataclass(frozen=True)
class MethodologyDefinition:
    """
    The immutable conceptual framework definition.
    """
    metadata: MethodologyMetadata

@dataclass(frozen=True)
class ProfileIdentity:
    """
    Immutable profile artifact ensuring reproducibility.
    """
    id: str
    semantic_version: str
    hash: str
    parent: Optional[str]
    created: datetime.datetime
    author: str
    compatibility: str
    signature: str

@dataclass(frozen=True)
class MethodologyInstance:
    """
    An execution-specific instance of a methodology bound to a profile.
    """
    definition: MethodologyDefinition
    profile_identity: ProfileIdentity
