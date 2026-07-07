from Backend.Platform15.contracts.dtos import RiskContextDTO, RiskReason
class PortfolioConstraintEngine:
    __version__ = 'v1.0'
    __dto_version__ = 'v1.0'
    __schema_version__ = 'v1.0'
    def execute(self, recommendation, context: RiskContextDTO):
        from Backend.Platform15.pipeline import EngineResult
        if context.available_buying_power <= 0:
            return EngineResult("FAIL", [RiskReason("INSUFFICIENT_BUYING_POWER", "HIGH", "Available BP is 0 or negative")])
        return EngineResult("PASS", [])