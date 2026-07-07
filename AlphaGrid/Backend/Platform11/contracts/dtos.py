from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

# Import foundational DTOs (using existing stubs)
from Backend.Platform10.contracts.dtos import ExecutionContext

@dataclass(frozen=True)
class MethodologyHistoryDTO:
    methodology_id: str
    current_reliability: float
    historical_reliability: float
    stability_30d: float

@dataclass(frozen=True)
class InteractionTraceDTO:
    source_methodology: str
    target_methodology: str
    rule_applied: str  # e.g., 'Increase Reliability', 'Reduce Applicability'
    impact_magnitude: float

@dataclass(frozen=True)
class CompositeTraceDTO:
    input_methodologies: List[str]
    interactions_applied: List[InteractionTraceDTO]
    conflicts_detected: int
    consensus_built: str
    evidence_generated: int
    intent_produced: str

@dataclass(frozen=True)
class CompositeHealthDTO:
    status: str  # Ready | Partial | Degraded | Unavailable
    missing_methodologies: List[str]
    active_methodologies: List[str]

@dataclass(frozen=True)
class CompositeMethodologyDTO:
    id: str
    schema_version: str
    composite_direction: str         # Bullish | Bearish | Neutral | Mixed
    composite_confidence: float      # 0.0 - 1.0 (Synthesized)
    composite_reliability: float     # 0.0 - 1.0
    composite_applicability: float   # 0.0 - 1.0
    
    # Multi-dimensional consensus
    direction_consensus: str         # Strong | Moderate | Weak | None
    confidence_consensus: str
    reliability_consensus: str
    regime_consensus: str
    structure_consensus: str
    
    conflict_severity: str           # Low | Medium | High | Critical
    
    # Contradiction graph representation
    contradiction_graph: Dict[str, str] # e.g. {'Trend': 'Bullish', 'Mean Reversion': 'Bearish'}
    
    dominant_methodologies: List[str]
    supporting_methodologies: List[str]
    conflicting_methodologies: List[str]
    
    applied_interaction_rules: List[str]
    
    composite_health: CompositeHealthDTO
    composite_trace: CompositeTraceDTO
    
    execution_context: ExecutionContext

@dataclass(frozen=True)
class CompositeDecisionContextDTO:
    """Normalized context prepared exclusively for Platform 12 (Capability Orchestrator).
    Platform 12 consumes this to decide if an opportunity exists, keeping Platform 11
    decision-neutral.
    """
    id: str
    timestamp: datetime
    numerical_intent: float          # Post-synthesis vector mapping (-1.0 to 1.0)
    composite_confidence: float
    regime_context: str
    structural_context: str
    volatility_context: str
    liquidity_context: str
    composite_methodology: CompositeMethodologyDTO
    execution_context: ExecutionContext
