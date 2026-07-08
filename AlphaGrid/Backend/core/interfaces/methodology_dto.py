from dataclasses import dataclass, field
from typing import Dict
from .methodology_provenance_dto import MethodologyProvenanceDTO

@dataclass(frozen=True)
class MethodologyDTO:
    """
    The pure analytical representation of a single methodology's state (e.g. ICT, SMC).
    Absolutely no execution, trading, entry, or exit signals allowed. 
    Platform 10 produces this object immutably.
    """
    id: str
    name: str
    semantic_bias: str # e.g. Bullish, Bearish, Neutral, Distribution, Accumulation
    confidence: float
    state: str # State machine state
    provenance: MethodologyProvenanceDTO
    metadata: Dict[str, str] = field(default_factory=dict)
