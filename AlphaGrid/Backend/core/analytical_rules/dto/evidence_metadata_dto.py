from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class EvidenceMetadataDTO:
    """Metadata detailing versions and execution parameters associated with this evidence."""
    schema_version: str
    rule_version: str
    rule_checksum: str
    registry_checksum: str
    sdk_version: str
    planner_version: str
    fingerprint: str
    custom_tags: Dict[str, Any]
