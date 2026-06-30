"""AI domain shared models."""

from uuid import UUID
from pydantic import Field
from .common import AlphaGridBaseModel


class AIModel(AlphaGridBaseModel):
    """An AI model registry metadata record."""

    model_id: UUID
    model_name: str = Field(..., min_length=1)
    version: str = Field(..., min_length=1)
    framework: str = Field(..., min_length=1)
    status: str = Field(..., min_length=1)
