from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class RiskContextDTO:
    account_equity: float
    available_buying_power: float
    daily_realized_pnl: float
    current_drawdown: float
    current_total_exposure: float
    user_risk_profile: str
    max_risk_per_trade_pct: float
    max_daily_loss_pct: float
    max_correlation_exposure: float

@dataclass(frozen=True)
class RiskReason:
    code: str
    severity: str
    evidence: str

@dataclass(frozen=True)
class RiskAssessmentDTO:
    recommendation_id: str
    decision: str
    recommended_position_size: float
    max_downside_usd: float
    reasons: List[RiskReason] = field(default_factory=list)
    provenance_chain: List[str] = field(default_factory=list)
