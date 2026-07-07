from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class AuditDTO:
    is_certified: bool
    certification_stage: str
    last_audit_timestamp: Optional[str]
    audit_hash: Optional[str]
