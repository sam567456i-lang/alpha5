"""Common base model configuration for AlphaGrid domain models."""

from pydantic import BaseModel, ConfigDict


class AlphaGridBaseModel(BaseModel):
    """Authoritative base model with shared validation configuration."""

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_assignment=True,
    )
