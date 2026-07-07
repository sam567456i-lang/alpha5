import os
import yaml

def scaffold_p16(repo_root: str):
    p16_dir = os.path.join(repo_root, "Backend", "Platform16")
    gov_dir = os.path.join(repo_root, "Docs", "Governance", "registry")
    
    # 1. Directories
    dirs = [
        "",
        "contracts",
        "engine",
        "adapters"
    ]
    for d in dirs:
        os.makedirs(os.path.join(p16_dir, d), exist_ok=True)
        
    os.makedirs(os.path.join(repo_root, "Backend", "tests", "platform16"), exist_ok=True)
        
    # 2. Files
    files = {
        "__init__.py": "# Platform 16: Portfolio Intelligence\n",
        "contracts/__init__.py": "",
        "contracts/dtos.py": '''from dataclasses import dataclass, field
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
''',
        "adapters/__init__.py": "",
        "adapters/risk_context_builder.py": '''
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
''',
        "engine/__init__.py": "",
        "pipeline.py": '''
from Backend.Platform16.contracts.dtos import PortfolioStateDTO, PortfolioAssessmentDTO
from Backend.Platform15.pipeline import RecommendationDTO
from typing import List

class PortfolioPipeline:
    def __init__(self):
        # We will dynamically load engines here like P15
        self.engines = []
        
    def execute(self, state: PortfolioStateDTO, recommendations: List[RecommendationDTO]) -> PortfolioAssessmentDTO:
        # Mocking pipeline for scaffolding
        gross_exposure = sum([p.size * p.current_price for p in state.positions]) / max(state.cash, 1.0)
        
        return PortfolioAssessmentDTO(
            gross_exposure=gross_exposure,
            net_exposure=0.0,
            health_status="HEALTHY" if gross_exposure < 1.0 else "WARNING"
        )
'''
    }

    for path, content in files.items():
        with open(os.path.join(p16_dir, path), "w", encoding="utf-8") as f:
            f.write(content)
            
    # 3. Governance Registries
    registries = [
        "portfolio_plugin_registry.yaml",
        "portfolio_policy_registry.yaml",
        "portfolio_limits_registry.yaml",
        "portfolio_scoring_registry.yaml"
    ]
    
    for reg in registries:
        with open(os.path.join(gov_dir, reg), "w") as f:
            f.write("# Placeholder for P16 Registry\n")

    print("Platform 16 Scaffolded.")

if __name__ == "__main__":
    repo = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    scaffold_p16(repo)
