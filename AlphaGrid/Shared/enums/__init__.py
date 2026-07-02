"""Shared enumeration definitions."""

from enum import StrEnum

class RecommendationStatus(StrEnum):
    NEW = "NEW"
    VALIDATED = "VALIDATED"
    ACTIVE = "ACTIVE"
    WEAKENING = "WEAKENING"
    EXPIRED = "EXPIRED"
    ARCHIVED = "ARCHIVED"

class TradeDirection(StrEnum):
    BUY = "BUY"
    SELL = "SELL"

class TradeStatus(StrEnum):
    PENDING = "PENDING"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"

class ResearchStatus(StrEnum):
    DRAFT = "DRAFT"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"

class NotificationSeverity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

from .signal_direction import SignalDirection
from .methodology_status import MethodologyStatus
from .experiment_status import ExperimentStatus
from .concept_type import ConceptType
from .timeframe import Timeframe
from .concept_state import (
    MomentumState,
    VolatilityState,
    ExtremumState,
    TrendState,
    BreakoutState,
    StrengthState
)

__all__ = [
    "RecommendationStatus",
    "TradeDirection",
    "TradeStatus",
    "ResearchStatus",
    "NotificationSeverity",
    "SignalDirection",
    "MethodologyStatus",
    "ExperimentStatus",
    "ConceptType",
    "Timeframe",
    "MomentumState",
    "VolatilityState",
    "ExtremumState",
    "TrendState",
    "BreakoutState",
    "StrengthState"
]
