from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# ==========================================
# Input DTOs (Consumed from Platform 9)
# ==========================================

@dataclass(frozen=True)
class ExecutionContext:
    timestamp: str
    environment: str
    run_id: str

@dataclass(frozen=True)
class FeatureSetDTO:
    features: Dict[str, float]

@dataclass(frozen=True)
class ConceptSetDTO:
    concepts: Dict[str, Any]

@dataclass(frozen=True)
class MarketStateDTO:
    symbol: str
    timeframe: str
    features: FeatureSetDTO
    concepts: ConceptSetDTO
    context: ExecutionContext

# ==========================================
# Intermediate Builder DTOs (Platform 10 Internal)
# ==========================================

@dataclass(frozen=True)
class ConfidenceFactorsDTO:
    factors: Dict[str, float]
    
@dataclass(frozen=True)
class EvidenceDTO:
    supporting_concepts: List[str]
    conflicting_concepts: List[str]
    raw_evidence: List[str]

@dataclass(frozen=True)
class ExplainabilityDTO:
    why_applicable: str
    why_not_applicable: str
    supporting_evidence_summary: str
    conflicting_evidence_summary: str
    required_conditions: str
    invalidating_conditions: str

# ==========================================
# Output DTO (Produced for Platform 11)
# ==========================================

@dataclass(frozen=True)
class MethodologyResultDTO:
    methodology_id: str
    version: str
    plugin_id: str
    execution_id: str
    execution_context: ExecutionContext
    score: float
    confidence: float
    strength: float
    evidence: EvidenceDTO
    supporting_concepts: List[str]
    conflicting_concepts: List[str]
    preconditions: List[str]
    failure_reasons: List[str]
    explainability: ExplainabilityDTO
    metadata: Dict[str, Any]
    execution_duration_ms: float
    validation_status: str
    
    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("Confidence must be between 0.0 and 1.0")
        if not (0.0 <= self.strength <= 1.0):
            raise ValueError("Strength must be between 0.0 and 1.0")

# ==========================================
# Metrics & Observability DTOs
# ==========================================

@dataclass(frozen=True)
class ExecutionTraceDTO:
    execution_id: str
    plugin_id: str
    stages_executed: List[str]
    dependencies_consumed: List[str]
    evidence_generated: EvidenceDTO
    confidence_factors: ConfidenceFactorsDTO
    final_confidence: float
    execution_duration_ms: float
    result: str # "SUCCESS", "SKIPPED", "ERROR"

@dataclass(frozen=True)
class PlatformMetricsDTO:
    methodologies_executed: int
    total_execution_time_ms: float
    success_rate: float
    failure_rate: float
    skipped: int
    dependency_failures: int
    cache_hits: int
    average_confidence: float
    average_runtime_ms: float

# ==========================================
# Core Methodology Profiles (Embedded in Metadata)
# ==========================================

@dataclass(frozen=True)
class ProvenanceDTO:
    factor: str
    weight: float
    contribution: float
    reason: str

@dataclass(frozen=True)
class MethodologyProfileDTO:
    methodology_id: str
    version: str
    health: str
    confidence: float
    reliability: float
    applicability: float
    provenance: List[ProvenanceDTO]
    evidence: EvidenceDTO
    explainability: ExplainabilityDTO
    execution_id: str
    execution_timestamp: str
    scheduler_cadence: str
    cache_status: str
    validation_status: str

@dataclass(frozen=True)
class TrendProfileDTO(MethodologyProfileDTO):
    direction: str       # Bullish | Bearish | Neutral
    strength: str        # Weak | Moderate | Strong | Extreme
    quality: str         # Poor | Fair | Good | Excellent
    persistence: str     # Low | Medium | High
    maturity: str        # Emerging | Established | Late | Exhausted
    regime: str          # Trending | Transition | Consolidating

@dataclass(frozen=True)
class MomentumProfileDTO(MethodologyProfileDTO):
    direction: str             # Bullish | Bearish | Neutral
    velocity: str              # Weak | Moderate | Strong | Extreme
    acceleration: str          # Increasing | Stable | Decreasing
    persistence: str           # Low | Medium | High
    exhaustion: str            # Low | Medium | High | Critical
    divergence: str            # None | Bullish Regular | Bearish Regular | Bullish Hidden | Bearish Hidden
    regime_compatibility: str  # Trending | Ranging | Transition

@dataclass(frozen=True)
class MeanReversionProfileDTO(MethodologyProfileDTO):
    state: str                 # Overextended Bullish | Overextended Bearish | Equilibrium
    reference_value_type: str  # VWAP | POC | Statistical | Dynamic
    deviation_severity: str    # Normal | High | Extreme | Unprecedented
    expected_horizon: str      # Immediate | Short | Medium | Long
    reversion_target: str      # Unknown | Weak | Primary | Secondary | Complete
    prob_initiation: float     # 0.0 - 1.0
    prob_completion: float     # 0.0 - 1.0
    prob_failure: float        # 0.0 - 1.0
    statistical_confidence: float # 0.0 - 1.0
    structural_confidence: float  # 0.0 - 1.0
    structure: str             # Rejection Formation | Consolidation | No Evidence
    regime_compatibility: str  # Trending | Ranging | Transition
    failure_conditions: List[str]

@dataclass(frozen=True)
class PriceActionProfileDTO(MethodologyProfileDTO):
    direction: str             # Bullish | Bearish | Neutral
    pattern_class: str         # Continuation | Reversal | Indecision
    strength: str              # Weak | Moderate | Strong | Extreme
    quality: str               # Poor | Fair | Good | Excellent
    context_compatibility: str # Low | Medium | High
    rejection_strength: float  # 0.0 - 1.0
    acceptance_strength: float # 0.0 - 1.0
    reversal_potential: float  # 0.0 - 1.0
    continuation_potential: float # 0.0 - 1.0

@dataclass(frozen=True)
class ICTProfileDTO(MethodologyProfileDTO):
    institutional_bias: str      # Bullish | Bearish | Neutral
    liquidity_target: str        # BSL | SSL | Internal | External
    displacement_strength: str   # Weak | Moderate | Strong
    market_structure_state: str  # Expansion | Retracement | Reversal | Consolidation
    killzone_alignment: bool
    time_of_day_context: str

@dataclass(frozen=True)
class WyckoffProfileDTO(MethodologyProfileDTO):
    phase: str                   # Phase A | Phase B | Phase C | Phase D | Phase E
    composite_operator_bias: str # Accumulation | Distribution
    spring_or_upthrust: bool
    sos_or_sow: bool
    markup_markdown_potential: str # Low | Moderate | High

@dataclass(frozen=True)
class FreshnessProfileDTO:
    generated_at: str
    freshness_class: str # Instant | Intrabar | Session | Swing | Structural | Persistent
    expiration_policy: str
    expires_at: Optional[str]
    confidence_decay_policy: str
    staleness_state: str # Fresh | Aging | Stale | Expired
    refresh_trigger: str # NewTick | NewBar | SessionChange | StructureChange | ManualRecompute

@dataclass(frozen=True)
class DataQualityProfileDTO:
    tick_completeness: float
    missing_packets: int
    feed_latency_ms: float
    timestamp_quality: str
    sequence_integrity: str
    provider_confidence: float

@dataclass(frozen=True)
class OrderFlowProfileDTO(MethodologyProfileDTO):
    absorption_strength: str
    participant_control: str # Passive Buyers | Aggressive Sellers | etc.
    delta_divergence_severity: str
    freshness: FreshnessProfileDTO
    data_quality: DataQualityProfileDTO

@dataclass(frozen=True)
class VolumeProfileProfileDTO(MethodologyProfileDTO):
    auction_state: str # Acceptance | Rejection
    profile_balance: str
    value_area_migration: str
    freshness: FreshnessProfileDTO
    data_quality: DataQualityProfileDTO

from Backend.shared_domain.contracts.dtos import LineageDTO, ConfidenceProfileDTO

@dataclass(frozen=True)
class MacroProfileDTO(MethodologyProfileDTO):
    regime: str
    central_bank_bias: str
    growth_inflation_matrix: str
    lineage: Optional[LineageDTO] = None
    confidence_profile: Optional[ConfidenceProfileDTO] = None

@dataclass(frozen=True)
class OptionsProfileDTO(MethodologyProfileDTO):
    net_gamma: str
    dealer_positioning: str
    volatility_premium: float
    lineage: Optional[LineageDTO] = None
    confidence_profile: Optional[ConfidenceProfileDTO] = None
    
@dataclass(frozen=True)
class MLProfileDTO(MethodologyProfileDTO):
    prediction_target: str
    probability_distribution: str
    feature_importance: str
    lineage: Optional[LineageDTO] = None
    confidence_profile: Optional[ConfidenceProfileDTO] = None
