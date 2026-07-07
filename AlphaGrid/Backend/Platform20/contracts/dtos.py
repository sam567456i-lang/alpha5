from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass(frozen=True)
class NotificationEventDTO:
    event_id: str
    event_type: str # e.g., OpportunityDetected, RiskRejected, ConfidenceDropped
    source_platform: str
    timestamp: str
    payload: Dict[str, Any]

@dataclass(frozen=True)
class NotificationPolicyDTO:
    policy_id: str
    target_channels: List[str]
    min_confidence: float
    markets: List[str]
    methodologies: List[str]

@dataclass(frozen=True)
class NotificationDTO:
    notification_id: str
    event_id: str
    title: str
    message: str
    priority: str
    target_channels: List[str]

@dataclass(frozen=True)
class NotificationHistoryDTO:
    notification_id: str
    event_id: str
    channel: str
    timestamp: str
    delivery_status: str
    suppression_reason: Optional[str]