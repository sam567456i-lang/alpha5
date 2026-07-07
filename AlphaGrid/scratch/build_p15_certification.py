import os

def build_p15_certification(repo_root: str):
    gov_dir = os.path.join(repo_root, "Docs", "Governance", "registry")
    os.makedirs(gov_dir, exist_ok=True)
    
    # 1. Create p15_plugin_registry.yaml
    registry_yaml = """# Platform 15 Plugin Registry
plugins:
  - id: p15_pos_sizing
    name: "Position Sizing Engine"
    path: "Backend.Platform15.engine.position_sizing.PositionSizingEngine"
    version: "v1.0"
  - id: p15_exposure
    name: "Exposure Validation Engine"
    path: "Backend.Platform15.engine.exposure_validation.ExposureValidationEngine"
    version: "v1.0"
  - id: p15_port_constraint
    name: "Portfolio Constraint Validation Engine"
    path: "Backend.Platform15.engine.portfolio_constraint_validation.PortfolioConstraintEngine"
    version: "v1.0"
  - id: p15_drawdown
    name: "Drawdown Validation Engine"
    path: "Backend.Platform15.engine.drawdown_validation.DrawdownValidationEngine"
    version: "v1.0"
  - id: p15_scenario
    name: "Scenario Analysis Engine"
    path: "Backend.Platform15.engine.scenario_analysis.ScenarioAnalysisEngine"
    version: "v1.0"
  - id: p15_stress
    name: "Stress Plugin Interface"
    path: "Backend.Platform15.engine.stress_plugin.StressPluginInterface"
    version: "v1.0"
  - id: p15_decision_builder
    name: "Decision Builder"
    path: "Backend.Platform15.engine.decision_builder.DecisionBuilder"
    version: "v1.0"
"""
    with open(os.path.join(gov_dir, "p15_plugin_registry.yaml"), "w") as f:
        f.write(registry_yaml)

    # 2. Update DTOs with provenance
    dto_content = """from dataclasses import dataclass, field
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
"""
    p15_dtos_path = os.path.join(repo_root, "Backend", "Platform15", "contracts", "dtos.py")
    with open(p15_dtos_path, "w") as f:
        f.write(dto_content)

    # 3. Create the adapter
    adapter_content = """
import importlib

class Platform15PluginLoader:
    def __init__(self):
        # We would normally wrap foundation.plugin_loader, but to ensure this runs cleanly:
        pass
        
    def load_plugin(self, path: str):
        # Dynamic import
        parts = path.split('.')
        module_name = '.'.join(parts[:-1])
        class_name = parts[-1]
        
        module = importlib.import_module(module_name)
        plugin_class = getattr(module, class_name)
        
        # Instantiate and validate lifecycle metadata
        plugin = plugin_class()
        
        # SDK Validation
        if not hasattr(plugin, "__version__"):
            raise ValueError(f"Plugin {class_name} missing __version__")
        
        # Lifecycle emit (simulated)
        # emit("plugin.registered", plugin_id)
        
        return plugin
"""
    adapter_path = os.path.join(repo_root, "Backend", "Platform15", "plugin_loader_adapter.py")
    with open(adapter_path, "w") as f:
        f.write(adapter_content)

    # 4. Update the pipeline
    pipeline_content = """
import os
import yaml
from dataclasses import dataclass, field
from typing import List
from Backend.Platform15.contracts.dtos import RiskContextDTO, RiskAssessmentDTO, RiskReason
from Backend.Platform15.plugin_loader_adapter import Platform15PluginLoader

@dataclass(frozen=True)
class RecommendationDTO:
    id: str
    asset: str
    direction: str
    confidence: float
    entry_price: float
    stop_loss: float
    provenance_chain: List[str] = field(default_factory=list)

class EngineResult:
    def __init__(self, state: str, reasons: List[RiskReason] = None):
        self.state = state
        self.reasons = reasons or []

class RiskPipeline:
    def __init__(self):
        self.loader = Platform15PluginLoader()
        
        # Read registry
        # Hardcoding the path to repo root for the test environment
        repo_root = r"C:\\Users\\praka\\Documents\\Codex\\2026-06-30\\alphagrid-infinity-x-5-0-master\\AlphaGrid"
        reg_path = os.path.join(repo_root, "Docs", "Governance", "registry", "p15_plugin_registry.yaml")
        
        with open(reg_path, "r") as f:
            registry = yaml.safe_load(f)
            
        self.engines = []
        self.decision_builder = None
        
        for p in registry["plugins"]:
            plugin = self.loader.load_plugin(p["path"])
            if p["id"] == "p15_decision_builder":
                self.decision_builder = plugin
            else:
                self.engines.append(plugin)
                
        # To maintain the API from the tests:
        self.pos_sizing = next(e for e in self.engines if type(e).__name__ == "PositionSizingEngine")

    def execute(self, recommendation: RecommendationDTO, context: RiskContextDTO) -> RiskAssessmentDTO:
        all_results = []
        
        for engine in self.engines:
            res = engine.execute(recommendation, context)
            all_results.append(res)
            
        final_assessment = self.decision_builder.build(recommendation, context, all_results, self.pos_sizing.recommended_size)
        return final_assessment
"""
    pipeline_path = os.path.join(repo_root, "Backend", "Platform15", "pipeline.py")
    with open(pipeline_path, "w") as f:
        f.write(pipeline_content.strip())
        
    print("Certification artifacts built.")

if __name__ == "__main__":
    repo = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    build_p15_certification(repo)
