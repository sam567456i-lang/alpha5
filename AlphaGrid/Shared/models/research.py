"""Research domain shared models."""

from datetime import datetime
from uuid import UUID
from pydantic import Field
from Shared.enums import ResearchStatus
from .common import AlphaGridBaseModel


class ResearchProject(AlphaGridBaseModel):
    """A research project tracking strategy design and experiments."""

    project_id: UUID
    title: str = Field(..., min_length=1)
    objective: str = Field(..., min_length=1)
    status: ResearchStatus
    created_at: datetime
