from dataclasses import dataclass, field
from typing import Dict, List, Any
from .execution_mode_dto import ExecutionModeDTO

@dataclass(frozen=True)
class MethodologyContextDTO:
    """
    The immutable, universal input envelope passed to every methodology runtime evaluation.
    Contains the absolute context required to build a methodology without external lookups.
    """
    identity: str
    market_identity: str
    symbol: str
    timeframe: str
    session: str
    registry_versions: Dict[str, str] = field(default_factory=dict)
    replay_metadata: Dict[str, Any] = field(default_factory=dict)
    concept_references: List[str] = field(default_factory=list)
    liquidity_references: List[str] = field(default_factory=list)
    structure_references: List[str] = field(default_factory=list)
    zone_references: List[str] = field(default_factory=list)
    quality_snapshot: Dict[str, float] = field(default_factory=dict)
    environment_metadata: Dict[str, Any] = field(default_factory=dict)
    execution_mode: ExecutionModeDTO = None
