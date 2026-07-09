from dataclasses import dataclass, field
from typing import List, Dict, Any
from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO

@dataclass(frozen=True)
class CrossMarketEvidenceDTO(EvidenceDTO):
    """Base class for cross-market objective relationships."""
    primary_symbol_id: str = ""
    secondary_symbol_id: str = ""

@dataclass(frozen=True)
class CorrelationEvidenceDTO(CrossMarketEvidenceDTO):
    """Objective correlation metric between two assets."""
    correlation_coefficient: float = 0.0
    rolling_window: int = 0
    metric_type: str = "PEARSON"

@dataclass(frozen=True)
class LeadLagEvidenceDTO(CrossMarketEvidenceDTO):
    """Objective lead/lag metric."""
    leader_symbol_id: str = ""
    lag_periods: int = 0
    confidence: float = 0.0

@dataclass(frozen=True)
class CointegrationEvidenceDTO(CrossMarketEvidenceDTO):
    """Objective cointegration metric."""
    is_cointegrated: bool = False
    p_value: float = 0.0

@dataclass(frozen=True)
class BetaEvidenceDTO(CrossMarketEvidenceDTO):
    """Objective beta metric."""
    beta_value: float = 1.0

@dataclass(frozen=True)
class RelativeStrengthEvidenceDTO(CrossMarketEvidenceDTO):
    """Objective relative strength metric."""
    rs_value: float = 1.0

@dataclass(frozen=True)
class VolatilityCouplingEvidenceDTO(CrossMarketEvidenceDTO):
    """Objective volatility coupling metric."""
    coupling_coefficient: float = 0.0

@dataclass(frozen=True)
class LiquidityCouplingEvidenceDTO(CrossMarketEvidenceDTO):
    """Objective liquidity coupling metric."""
    coupling_coefficient: float = 0.0

@dataclass(frozen=True)
class MarketRegimeEvidenceDTO(EvidenceDTO):
    """Base class for market regime evidence."""
    symbol_id: str = ""
    confidence: float = 0.0

@dataclass(frozen=True)
class TrendRegimeEvidenceDTO(MarketRegimeEvidenceDTO):
    trend_type: str = "BULLISH" # BULLISH, BEARISH, NEUTRAL

@dataclass(frozen=True)
class LiquidityRegimeEvidenceDTO(MarketRegimeEvidenceDTO):
    liquidity_state: str = "HIGH" # HIGH, LOW, NORMAL

@dataclass(frozen=True)
class VolatilityRegimeEvidenceDTO(MarketRegimeEvidenceDTO):
    volatility_state: str = "EXPANSION" # EXPANSION, COMPRESSION

@dataclass(frozen=True)
class ParticipationRegimeEvidenceDTO(MarketRegimeEvidenceDTO):
    participation_level: str = "INSTITUTIONAL" # INSTITUTIONAL, RETAIL

@dataclass(frozen=True)
class MacroRegimeEvidenceDTO(MarketRegimeEvidenceDTO):
    macro_state: str = "RISK_ON" # RISK_ON, RISK_OFF

@dataclass(frozen=True)
class ScheduledEventEvidenceDTO(EvidenceDTO):
    """Objective scheduled market event (e.g. FOMC, NFP)."""
    event_name: str = "" 
    impact_level: str = "HIGH"
    affected_symbols: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class ObservedEventEvidenceDTO(EvidenceDTO):
    """Objective observed market event (e.g. Gap, Circuit Breaker)."""
    event_type: str = "GAP"
    severity: str = "HIGH"
    affected_symbols: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class ComparisonEvidenceDTO(EvidenceDTO):
    """Objective comparison of N assets."""
    comparison_id: str = ""
    symbols: List[str] = field(default_factory=list)
    window: int = 0
    metric: str = ""
    policy: str = ""
    confidence: float = 0.0
    sample_size: int = 0
    time_alignment: str = "STRICT"
    quality_score: float = 1.0
    comparison_type: str = "STRUCTURAL"
    results: Dict[str, Any] = field(default_factory=dict)
