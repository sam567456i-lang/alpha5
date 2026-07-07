from Backend.Platform15.contracts.dtos import RiskContextDTO, RiskReason
class DrawdownValidationEngine:
    __version__ = 'v1.0'
    __dto_version__ = 'v1.0'
    __schema_version__ = 'v1.0'
    def execute(self, recommendation, context: RiskContextDTO):
        from Backend.Platform15.pipeline import EngineResult
        if context.current_drawdown > context.max_daily_loss_pct:
            return EngineResult("FAIL", [RiskReason("MAX_DAILY_LOSS", "HIGH", f"Drawdown {context.current_drawdown}% exceeds limit")])
        return EngineResult("PASS", [])