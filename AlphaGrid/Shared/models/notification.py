"""Notification domain shared models."""

from datetime import datetime
from uuid import UUID
from pydantic import Field
from Shared.enums import NotificationSeverity
from .common import AlphaGridBaseModel


class Notification(AlphaGridBaseModel):
    """System alert or user notification."""

    notification_id: UUID
    title: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    severity: NotificationSeverity
    created_at: datetime
    is_read: bool = Field(default=False)
