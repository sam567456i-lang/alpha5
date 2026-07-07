from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class RuntimeTraceDTO:
    raw_tick_ids: List[str]
    snapshot_id: str
    geometry_uuids: List[str]
    feature_uuids: List[str]
    concept_uuids: List[str]
    methodology_uuid: Optional[str]
    pipeline_stage: str
    schema_version: str

@dataclass(frozen=True)
class SemanticTraceDTO:
    sources: List[str]
    reasoning: str

@dataclass(frozen=True)
class LineageDTO:
    runtime: RuntimeTraceDTO
    semantic: SemanticTraceDTO
