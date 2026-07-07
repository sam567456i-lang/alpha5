
from Backend.Platform16.contracts.dtos import PortfolioStateDTO, PortfolioAssessmentDTO
from Backend.Platform15.contracts.dtos import RiskContextDTO

class RiskContextBuilder:
    """Translates Portfolio state/assessment into P15's native RiskContextDTO"""
    @staticmethod
    def build(state: PortfolioStateDTO, assessment: PortfolioAssessmentDTO) -> RiskContextDTO:
        equity = state.cash + sum([(p.current_price * p.size) for p in state.positions])
        return RiskContextDTO(
            account_equity=equity,
            available_buying_power=state.cash, # simplistic mockup
            daily_realized_pnl=state.daily_realized_pnl,
            current_drawdown=0.0,
            current_total_exposure=assessment.gross_exposure,
            user_risk_profile="MODERATE",
            max_risk_per_trade_pct=1.0,
            max_daily_loss_pct=5.0,
            max_correlation_exposure=0.5
        )
