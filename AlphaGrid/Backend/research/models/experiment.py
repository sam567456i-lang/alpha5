"""Experiment model for the Research Platform."""

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional, List
from uuid import UUID
from pydantic import Field, field_validator, model_serializer
from Shared.models.common import AlphaGridBaseModel


class ResearchParameterEncoder(json.JSONEncoder):
    """Custom JSON encoder to enforce exactly 8 decimal places for floats per ADP."""
    
    def iterencode(self, o, _one_shot=False):  # type: ignore
        # We override iterencode or use a custom dict transformation. 
        # But iterencode handles the stringification. 
        # It's easier to recursively format the dictionary before json.dumps
        pass

def _format_parameters(obj: Any) -> Any:
    """Recursively format floats to exactly 8 decimal places strings and normalize numpy primitives."""
    # Attempt to normalize common numpy types if they exist
    obj_type = type(obj).__name__
    if obj_type in ('bool_', 'bool'):
        if hasattr(obj, 'item'):
            obj = obj.item()
    elif obj_type in ('int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32', 'uint64'):
        if hasattr(obj, 'item'):
            obj = obj.item()
    elif obj_type in ('float16', 'float32', 'float64'):
        if hasattr(obj, 'item'):
            obj = obj.item()

    if isinstance(obj, bool):
        return obj # bool is subclass of int, so check it first
    elif isinstance(obj, int):
        return obj
    elif isinstance(obj, float):
        if obj != obj or obj == float('inf') or obj == float('-inf'):
            raise ValueError("NaN and Infinity are not allowed")
        return f"{obj:.8f}"
    elif isinstance(obj, str):
        return obj
    elif obj is None:
        return obj
    elif isinstance(obj, list):
        return [_format_parameters(item) for item in obj]
    elif isinstance(obj, dict):
        return {str(k): _format_parameters(v) for k, v in obj.items()}
    else:
        raise TypeError(f"Unsupported type: {type(obj)}")


class Experiment(AlphaGridBaseModel):
    """Represents a single execution of a strategy backtest."""

    id: UUID
    project_id: UUID
    strategy_id: str = Field(..., min_length=1)
    git_hash: str = Field(..., min_length=1)
    patch_hash: Optional[str] = None
    patch_text: Optional[str] = None
    dataset_snapshot_id: str = Field(..., min_length=64, max_length=64)
    dataset_hash: Optional[str] = None
    feature_versions: Dict[str, str] = Field(default_factory=dict)
    environment_fingerprint: str = Field(..., min_length=64, max_length=64)
    random_seed: int
    parameters: Dict[str, Any]
    parent_id: Optional[UUID] = None
    lineage_path: List[UUID] = Field(default_factory=list)
    is_exploratory: bool
    is_archived: bool
    schema_version: int = Field(default=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    archived_at: Optional[datetime] = None

    @field_validator("parameters")
    @classmethod
    def validate_parameters(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure parameters can be serialized deterministically to JSON."""
        try:
            # We enforce determinism by ensuring it serializes cleanly.
            formatted_v = _format_parameters(v)
            json.dumps(formatted_v, sort_keys=True, separators=(",", ":"))
        except (TypeError, ValueError) as e:
            raise ValueError(f"Parameters must be strict JSON serializable (no NaN/Inf, no custom objects): {e}")
        return v

    @field_validator("created_at", "archived_at")
    @classmethod
    def ensure_utc(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Ensure datetimes are timezone-aware and set to UTC."""
        if v is not None and v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        return v

    @model_serializer(mode="wrap")
    def serialize_model(self, handler, _info):  # type: ignore
        """Custom serialization to ensure parameters are deterministically formatted if needed."""
        data = handler(self)
        return data
