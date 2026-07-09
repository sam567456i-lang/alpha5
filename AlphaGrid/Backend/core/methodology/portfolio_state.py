from dataclasses import dataclass

@dataclass
class PortfolioState:
    """
    Objective state of the portfolio.
    """
    current_balance: float = 100000.0
    open_risk_pct: float = 0.0
    daily_realized_pnl_pct: float = 0.0
    max_daily_risk_pct: float = 3.0
    max_open_risk_pct: float = 2.0
