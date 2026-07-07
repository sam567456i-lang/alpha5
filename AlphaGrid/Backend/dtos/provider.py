from dataclasses import dataclass
from datetime import datetime
from typing import Optional

class ProviderStatus:
    HEALTHY = 'HEALTHY'
    DEGRADED = 'DEGRADED'
    DISCONNECTED = 'DISCONNECTED'

@dataclass
class ProviderHealth:
    provider_id: str
    status: str
    latency_ms: float
    packet_loss_percent: float
    reconnect_count: int
    last_heartbeat: datetime
    dropped_messages: int
    gap_frequency: float
    sequence_errors: int
    availability_percent: float

@dataclass(frozen=True)
class DataQualityScore:
    overall_score: float
    timestamp_score: float
    provider_score: float
    exchange_score: float
    sequence_score: float
    gap_score: float
    duplicate_score: float
    latency_score: float
    spread_score: float
    ohlc_score: float
    volume_score: float
    session_score: float
    corporate_action_score: float
    clock_drift_score: float
