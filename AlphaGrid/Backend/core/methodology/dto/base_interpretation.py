from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from Backend.core.methodology.dto.interpretation_identity import InterpretationIdentity

@dataclass(frozen=True)
class BaseInterpretation:
    """
    Root base class for all subjective interpretations.
    """
    identity: InterpretationIdentity
    metadata: Dict[str, Any] = field(default_factory=dict)
    lifecycle_status: str = "PENDING"  # Candidate -> Pending -> Evaluated -> Confirmed -> Superseded -> Archived

@dataclass(frozen=True)
class ContextInterpretation(BaseInterpretation):
    context_type: str = ""

@dataclass(frozen=True)
class BiasInterpretation(BaseInterpretation):
    bias_direction: str = ""

@dataclass(frozen=True)
class StructureInterpretation(BaseInterpretation):
    structure_type: str = ""
    
@dataclass(frozen=True)
class SessionInterpretation(BaseInterpretation):
    active_sessions: List[str] = field(default_factory=list)
    is_silver_bullet: bool = False

@dataclass(frozen=True)
class TargetInterpretation(BaseInterpretation):
    target_price: float = 0.0

@dataclass(frozen=True)
class SetupInterpretation(BaseInterpretation):
    setup_name: str = ""
    setup_direction: str = ""
    is_active: bool = False

@dataclass(frozen=True)
class EntryInterpretation(BaseInterpretation):
    entry_type: str = ""
    entry_price: float = 0.0
    stop_loss_price: float = 0.0
    target_price: float = 0.0

@dataclass(frozen=True)
class RiskInterpretation(BaseInterpretation):
    risk_profile: str = ""

@dataclass(frozen=True)
class ConflictInterpretation(BaseInterpretation):
    conflict_type: str = ""

@dataclass(frozen=True)
class ConfidenceInterpretation(BaseInterpretation):
    confidence_level: float = 0.0

@dataclass(frozen=True)
class NarrativeInterpretation(BaseInterpretation):
    narrative_text: str = ""

@dataclass(frozen=True)
class ConfluenceInterpretation(BaseInterpretation):
    component_interpretation_ids: List[str] = field(default_factory=list)
    component_candidate_ids: List[str] = field(default_factory=list)
    evaluation_ids: List[str] = field(default_factory=list)
    profile_identity: str = ""
    policy_identity: str = ""

@dataclass(frozen=True)
class SequenceInterpretation(BaseInterpretation):
    sequence_pattern: str = ""
    event_order: List[str] = field(default_factory=list)
    constraints_satisfied: bool = False
    coverage: float = 0.0
    confidence_sources: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class CrossMarketInterpretation(BaseInterpretation):
    divergence_type: str = ""
    primary_symbol: str = ""
    secondary_symbol: str = ""
    bias_indication: str = ""

@dataclass(frozen=True)
class AuctionInterpretation(BaseInterpretation):
    acceptance_state: str = "" # ACCEPTED, REJECTED, BALANCE
    region_type: str = ""
    value_area_shift: str = ""
