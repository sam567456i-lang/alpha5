from dataclasses import dataclass
from typing import Optional
import datetime

@dataclass(frozen=True)
class InterpretationIdentity:
    """
    Independent identity for an interpretation, ensuring full traceability.
    """
    id: str
    methodology_id: str
    profile_id: str
    evaluation_id: str
    candidate_id: str
    version: str
    hash: str
    created: datetime.datetime
    sequence: int
    timeframe: str
