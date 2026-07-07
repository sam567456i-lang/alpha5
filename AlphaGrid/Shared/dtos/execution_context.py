from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ExecutionContext:
    """
    Mandatory context for every immutable object in AlphaGrid.
    Guarantees deterministic replay, distributed debugging, observability, auditing, and event lineage.
    """
    session_id: str
    trace_id: str
    correlation_id: str
    instrument_id: str
    environment: str
    runtime_mode: str
    exchange: str
    provider: str
    market: str
    timezone: str
    sequence_id: int
    is_replay: bool
    build_version: str
    user_profile: Optional[str] = None
