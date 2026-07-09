import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from Backend.core.methodology.narrative_types import NarrativeNodeType, MethodologyType, NarrativeStage

@dataclass(frozen=True)
class NarrativeIdentity:
    """
    Rigid tracking for methodological provenance and replayability.
    """
    methodology: MethodologyType
    plugin_version: str
    rule_version: str
    graph_namespace: str
    timeframe: str
    creation_sequence: int

@dataclass(frozen=True)
class NarrativeNode:
    """
    Subjective state representing a methodology's interpretation of objective evidence.
    Completely decoupled from the EvidenceGraph; only stores string references.
    """
    node_id: str
    concept_type: NarrativeNodeType
    concept_name: str
    stage: NarrativeStage = NarrativeStage.CONTEXT
    identity: Optional[NarrativeIdentity] = None
    
    generated_at: str = field(default_factory=lambda: str(time.time()))
    
    # Provenance details: Why do I exist? Which plugin? Which policy?
    producer_plugin: str = ""
    producer_policy: str = ""

    
    # The objective evidence that backs this narrative
    supporting_evidence_ids: List[str] = field(default_factory=list)
    
    # Sub-narratives that form this composite narrative
    supporting_narrative_ids: List[str] = field(default_factory=list)
    
    # Componentized confidence vectors
    confidence_inputs: Dict[str, float] = field(default_factory=dict)

@dataclass(frozen=True)
class BiasNode(NarrativeNode):
    """
    Directional Bias Node (e.g. Bullish, Bearish, Neutral)
    Explicitly tracks the evidence domains that support this bias.
    """
    direction: str = "NEUTRAL"
    supported_by_structure: bool = False
    supported_by_liquidity: bool = False
    supported_by_regions: bool = False

@dataclass(frozen=True)
class POINode(NarrativeNode):
    """
    Point of Interest Node
    A generic region filtered through the lens of a specific methodology.
    """
    poi_type: str = "GENERIC"  # e.g., "Order Block", "FVG", "Session Level"
    is_active: bool = True

@dataclass(frozen=True)
class MarketContextNode(NarrativeNode):
    """
    Centralized reference aggregator for the CONTEXT stage.
    Owns no logic, merely collects references to orient downstream plugins.
    """
    bias_node_id: Optional[str] = None
    dealing_range_node_id: Optional[str] = None
    premium_discount_node_id: Optional[str] = None
    session_node_id: Optional[str] = None
    predecessor_node_id: Optional[str] = None
    
    poi_node_ids: List[str] = field(default_factory=list)
    timeframe_alignment_node_ids: List[str] = field(default_factory=list)
    active_regions: List[str] = field(default_factory=list)
    current_liquidity_map: List[str] = field(default_factory=list)
    active_structure_narrative_ids: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class LiquidityCandidateNode(NarrativeNode):
    """
    Intermediate candidate evaluation for a liquidity target.
    """
    priority_score: int = 0
    ranking_components: Dict[str, float] = field(default_factory=dict)

@dataclass(frozen=True)
class LiquidityTargetNode(NarrativeNode):
    """
    Methodological draw on liquidity.
    References the winning candidate instead of recomputing scores.
    """
    candidate_node_id: str = ""

@dataclass(frozen=True)
class StructureCandidateNode(NarrativeNode):
    """
    Intermediate candidate evaluation for a structural break.
    """
    proposed_label: str = "" # e.g. CHOCH, BOS, MSS
    alignment_with_context: bool = False
    is_multi_timeframe_confirmed: bool = False

@dataclass(frozen=True)
class StructureNarrativeNode(NarrativeNode):
    """
    Methodology-specific interpretation of a structural break.
    """
    structure_label: str = "" # e.g. CHOCH, BOS, MSS, SOS
    candidate_node_id: str = ""

@dataclass(frozen=True)
class DealingRangeNode(NarrativeNode):
    """
    Subjective dealing range derived from objective geometry, structural narratives, and market context.
    """
    objective_range_id: str = ""
    swing_high_id: str = ""
    swing_low_id: str = ""
    # Optional cached prices derived from the objective anchors
    range_high_price_cached: float = 0.0
    range_low_price_cached: float = 0.0
    is_premium_discount_active: bool = True

@dataclass(frozen=True)
class PDArrayNode(NarrativeNode):
    """
    Defines a narrative relationship between an objective region and a dealing range.
    """
    array_type: str = "" # e.g. "FVG", "OB", "Breaker"
    classification: str = "" # e.g. "Premium", "Discount", "Equilibrium"
    dealing_range_node_id: str = ""

@dataclass(frozen=True)
class TradeSetupNode(NarrativeNode):
    """
    Groups multiple potential entry models under a single market setup.
    """
    setup_direction: str = "" # e.g. "BULLISH", "BEARISH"
    is_active: bool = True

@dataclass(frozen=True)
class RetracementCandidateNode(NarrativeNode):
    """
    Candidate geometry for a Retracement entry model.
    """
    entry_price: float = 0.0
    stop_loss_price: float = 0.0
    target_price: float = 0.0
    fib_level: float = 0.0

@dataclass(frozen=True)
class EntryModelNode(NarrativeNode):
    """
    Formalized executable entry trigger that has passed methodological policies.
    """
    entry_type: str = "" # e.g. "OTE", "FVG Mitigation"
    entry_price: float = 0.0
    stop_loss_price: float = 0.0
    target_price: float = 0.0
    candidate_node_id: str = ""

@dataclass(frozen=True)
class SessionContextNode(NarrativeNode):
    """
    Objective tracking of active trading sessions and time windows.
    """
    active_session_ids: List[str] = field(default_factory=list) # e.g. "ASIA", "LONDON"
    active_time_window_ids: List[str] = field(default_factory=list) # e.g. "08:30-09:30"
    active_calendar_event_ids: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class NarrativeSequenceNode(NarrativeNode):
    """
    Models a chronological sequence of narrative nodes (e.g. Bias -> Sweep -> CHOCH -> OTE -> Entry).
    Essential for temporal models like AMD (Accumulation, Manipulation, Distribution) or Judas Swing.
    """
    sequence_type: str = "" # e.g. "AMD", "Judas_Swing"
    ordered_narrative_ids: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class ConfluenceCandidateNode(NarrativeNode):
    """
    Candidate for a multi-narrative setup (e.g. FVG + Breaker).
    """
    intersecting_narrative_ids: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class SessionSetupCandidateNode(NarrativeNode):
    """
    Candidate for a time-based setup (e.g. Silver Bullet).
    """
    session_context_id: str = ""
    trigger_narrative_ids: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class FeatureVectorNode(NarrativeNode):
    """
    Neutral extracted features for scoring.
    """
    setup_id: str = ""
    features: dict = field(default_factory=dict)

@dataclass(frozen=True)
class ScoreResultNode(NarrativeNode):
    """
    Methodology-specific score for a setup.
    """
    setup_id: str = ""
    score: float = 0.0
    grade: str = "" # e.g. "A", "B", "C"

@dataclass(frozen=True)
class DecisionNode(NarrativeNode):
    """
    Decision on whether to execute a setup.
    """
    setup_id: str = ""
    decision: str = "" # EXECUTE, DELAY, IGNORE, WAIT, CANCEL
    reasoning: str = ""

@dataclass(frozen=True)
class ExecutionPlanNode(NarrativeNode):
    """
    Plan for execution (sizing, stops, targets).
    """
    decision_id: str = ""
    entry_price: float = 0.0
    stop_price: float = 0.0
    target_price: float = 0.0
    position_size: float = 0.0
    order_type: str = ""

@dataclass(frozen=True)
class PositionNode(NarrativeNode):
    """
    An active, live execution in the market.
    """
    plan_id: str = ""
    status: str = "" # OPEN, CLOSED
    current_size: float = 0.0
    average_entry_price: float = 0.0

@dataclass(frozen=True)
class ManagementNode(NarrativeNode):
    """
    Active management of a position (e.g., scaling, partials).
    """
    position_id: str = ""
    action_type: str = "" # SCALE_IN, PARTIAL_TP, MOVE_STOP
    details: str = ""

@dataclass(frozen=True)
class ExitNode(NarrativeNode):
    """
    Terminal state of a position.
    """
    position_id: str = ""
    exit_reason: str = "" # STOP_HIT, TARGET_HIT, MANUAL, TIME_STOP
    realized_pnl: float = 0.0

@dataclass(frozen=True)
class RiskNarrativeNode(NarrativeNode):
    """
    Context on portfolio risk constraints.
    """
    risk_level: str = ""
    warning_message: str = ""














