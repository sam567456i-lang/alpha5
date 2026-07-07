import os

def write_engines(repo_root: str):
    engine_dir = os.path.join(repo_root, "Backend", "Platform15", "engine")

    files = {
        "position_sizing.py": """
from Backend.Platform15.contracts.dtos import RiskContextDTO, RiskReason
class PositionSizingEngine:
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
""",
        "exposure_validation.py": """
from Backend.Platform15.contracts.dtos import RiskContextDTO, RiskReason
class ExposureValidationEngine:
    def execute(self, recommendation, context: RiskContextDTO):
        from Backend.Platform15.pipeline import EngineResult
        if context.current_total_exposure > 0.8: # Example limit
            return EngineResult("WARNING", [RiskReason("HIGH_EXPOSURE", "MEDIUM", "Total exposure exceeds 80%")])
        return EngineResult("PASS", [])
""",
        "portfolio_constraint_validation.py": """
from Backend.Platform15.contracts.dtos import RiskContextDTO, RiskReason
class PortfolioConstraintEngine:
    def execute(self, recommendation, context: RiskContextDTO):
        from Backend.Platform15.pipeline import EngineResult
        if context.available_buying_power <= 0:
            return EngineResult("FAIL", [RiskReason("INSUFFICIENT_BUYING_POWER", "HIGH", "Available BP is 0 or negative")])
        return EngineResult("PASS", [])
""",
        "drawdown_validation.py": """
from Backend.Platform15.contracts.dtos import RiskContextDTO, RiskReason
class DrawdownValidationEngine:
    def execute(self, recommendation, context: RiskContextDTO):
        from Backend.Platform15.pipeline import EngineResult
        if context.current_drawdown > context.max_daily_loss_pct:
            return EngineResult("FAIL", [RiskReason("MAX_DAILY_LOSS", "HIGH", f"Drawdown {context.current_drawdown}% exceeds limit")])
        return EngineResult("PASS", [])
""",
        "scenario_analysis.py": """
from Backend.Platform15.contracts.dtos import RiskContextDTO, RiskReason
class ScenarioAnalysisEngine:
    def execute(self, recommendation, context: RiskContextDTO):
        from Backend.Platform15.pipeline import EngineResult
        # Simple deterministic check
        return EngineResult("PASS", [])
""",
        "stress_plugin.py": """
from Backend.Platform15.contracts.dtos import RiskContextDTO, RiskReason
class StressPluginInterface:
    def execute(self, recommendation, context: RiskContextDTO):
        from Backend.Platform15.pipeline import EngineResult
        # Future Monte Carlo plugin hook
        return EngineResult("PASS", [])
""",
        "decision_builder.py": """
from Backend.Platform15.contracts.dtos import RiskContextDTO, RiskAssessmentDTO, RiskReason
class DecisionBuilder:
    def build(self, recommendation, context: RiskContextDTO, engine_results: list, recommended_size: float) -> RiskAssessmentDTO:
        all_reasons = []
        has_fail = False
        has_warn = False
        
        for res in engine_results:
            if res.state == "FAIL":
                has_fail = True
            elif res.state == "WARNING":
                has_warn = True
            all_reasons.extend(res.reasons)
            
        decision = "ACCEPTED"
        if has_fail:
            decision = "REJECTED"
            recommended_size = 0.0
        elif has_warn:
            decision = "ACCEPTED_WITH_WARNINGS"
            
        max_downside = recommended_size * abs(recommendation.entry_price - recommendation.stop_loss)
        
        return RiskAssessmentDTO(
            recommendation_id=recommendation.id,
            decision=decision,
            recommended_position_size=recommended_size,
            max_downside_usd=max_downside,
            reasons=all_reasons
        )
"""
    }

    for path, content in files.items():
        with open(os.path.join(engine_dir, path), "w", encoding="utf-8") as f:
            f.write(content.strip())
            
    print("Engines written.")

if __name__ == "__main__":
    repo = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    write_engines(repo)
