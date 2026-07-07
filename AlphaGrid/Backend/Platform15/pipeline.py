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
        repo_root = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
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