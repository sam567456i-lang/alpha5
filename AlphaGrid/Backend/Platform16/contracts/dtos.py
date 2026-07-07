from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class PositionDTO:
    asset: str
    size: float
    entry_price: float
    current_price: float
    sector: str

@dataclass(frozen=True)
class PortfolioStateDTO:
    """Current factual state of the portfolio."""
    cash: float
    positions: List[PositionDTO]
    daily_realized_pnl: float

@dataclass(frozen=True)
class PortfolioAssessmentDTO:
    """Analysis of the portfolio state."""
    gross_exposure: float
    net_exposure: float
    health_status: str # 'HEALTHY', 'WARNING', 'CRITICAL'
    warnings: List[str] = field(default_factory=list)
