"""Shared enumeration definitions."""

from enum import StrEnum


class RecommendationStatus(StrEnum):
    """Recommendation status lifecycle states."""

    NEW = "NEW"
    VALIDATED = "VALIDATED"
    ACTIVE = "ACTIVE"
    WEAKENING = "WEAKENING"
    EXPIRED = "EXPIRED"
    ARCHIVED = "ARCHIVED"


class TradeDirection(StrEnum):
    """Direction of a trade order."""

    BUY = "BUY"
    SELL = "SELL"


class TradeStatus(StrEnum):
    """Trade execution states."""

    PENDING = "PENDING"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"


class ResearchStatus(StrEnum):
    """Research project or experiment states."""

    DRAFT = "DRAFT"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"


class NotificationSeverity(StrEnum):
    """System severity states for notifications."""

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
