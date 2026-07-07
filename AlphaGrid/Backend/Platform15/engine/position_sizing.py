from Backend.Platform15.contracts.dtos import RiskContextDTO, RiskReason
class PositionSizingEngine:
    __version__ = 'v1.0'
    __dto_version__ = 'v1.0'
    __schema_version__ = 'v1.0'
    def __init__(self):
        self.recommended_size = 0.0
    def execute(self, recommendation, context: RiskContextDTO):
        # Default: Fixed Fractional (e.g. 1% of account equity)
        risk_amount = context.account_equity * (context.max_risk_per_trade_pct / 100)
        stop_dist = abs(recommendation.entry_price - recommendation.stop_loss)
        if stop_dist > 0:
            self.recommended_size = risk_amount / stop_dist
        else:
            self.recommended_size = 0.0
        
        from Backend.Platform15.pipeline import EngineResult
        return EngineResult("PASS", [])