import os

def scaffold_platform18_and_manifests(repo_root: str):
    gov_dir = os.path.join(repo_root, "Docs", "Governance")
    
    # 1. Decision Intelligence Manifest
    manifest_content = """# Decision Intelligence Manifest

This document serves as the definitive operational contract for the entire AlphaGrid decision pipeline (Platforms 9 through 16).

## Platform 9: Concept Generation
- **Allowed Inputs**: GeometryDTO, FeatureSetDTO
- **Allowed Outputs**: ConceptSetDTO (with LineageDTO)
- **Decisions Produced**: Concept Existence, Relationship Topology
- **Decisions Forbidden**: Trading Signals, Methodology Evaluation
- **Registry Dependencies**: Concept Registry
- **Performance Budget**: Max Latency < 2ms per concept
- **Explainability**: Must provide semantic source mappings.

## Platform 10: Methodology Ecosystem
- **Allowed Inputs**: ConceptSetDTO
- **Allowed Outputs**: MethodologyResultDTO (with LineageDTO, FreshnessProfileDTO, ConfidenceProfileDTO, DataQualityProfileDTO)
- **Decisions Produced**: Directional Bias, Factor Confidence
- **Decisions Forbidden**: Execution Routing, Portfolio Allocation
- **Registry Dependencies**: Methodology Registry, Explainability Registry
- **Performance Budget**: Varies by Wave (e.g., Order Flow < 10ms)
- **Explainability**: Must populate EvidenceDTO strictly.

## Platform 18: Evidence & Explainability
- **Allowed Inputs**: ALL Pipeline DTOs (MethodologyResultDTO, PortfolioStateDTO, etc.)
- **Allowed Outputs**: ExplainabilityReportDTO, VisualizationRequestDTO
- **Decisions Produced**: Semantic Explanations, Conflict Resolution Narrative
- **Decisions Forbidden**: Generating Net-New Trading Recommendations, Recalculating Math
- **Registry Dependencies**: Explainability Registry
- **AI Permissions**: Read-Only access via Platform 22. AI cannot bypass P18 logic.
- **Human Approval**: Not required for explainability generation, but explanations support manual trade approval.
"""
    with open(os.path.join(gov_dir, "Decision_Intelligence_Manifest.md"), "w") as f:
        f.write(manifest_content.strip())
        
    # 2. Explainability Registry
    registry_dir = os.path.join(gov_dir, "registry")
    os.makedirs(registry_dir, exist_ok=True)
    explain_reg_content = """# Master Explainability Registry
dto_explanations:
  adjusted_confidence: "Confidence after penalties and supporting evidence were applied."
  staleness_state: "Indicates whether the analytical result is still considered current based on its freshness profile."
  derived_from: "References the upstream analytical object (Feature/Geometry) that produced this concept."
  raw_confidence: "The base statistical probability of the methodology before external market factors are applied."
  confidence_sources: "The specific features or concepts that actively increased the confidence score."
  penalties: "Market conditions or conflicting concepts that reduced the confidence score."
  freshness_class: "The expected lifetime category (e.g., Instant, Intrabar, Session, Swing) of the signal."
"""
    with open(os.path.join(registry_dir, "explainability_registry.yaml"), "w") as f:
        f.write(explain_reg_content.strip())
        
    # 3. Platform 18 DTOs
    p18_contracts = os.path.join(repo_root, "Backend", "Platform18", "contracts")
    os.makedirs(p18_contracts, exist_ok=True)
    
    p18_dtos = """
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass(frozen=True)
class VisualizationRequestDTO:
    visualization_type: str # e.g., Volume Profile, Delta Heatmap, Trend Lines
    data_source: str
    time_range_start: str
    time_range_end: str
    highlighted_entities: List[str]
    priority: str
    purpose: str

@dataclass(frozen=True)
class ExplainabilityReportDTO:
    report_id: str
    execution_timestamp: str
    target_recommendation_id: Optional[str]
    executive_summary: str
    decision_summary: str
    evidence_summary: str
    supporting_evidence: List[str]
    conflicting_evidence: List[str]
    confidence_analysis: str
    freshness_analysis: str
    risk_summary: str
    lineage_summary: str
    methodology_contributions: Dict[str, str]
    recommendations_for_further_review: List[str]
    visualization_requests: List[VisualizationRequestDTO]
"""
    with open(os.path.join(p18_contracts, "dtos.py"), "w") as f:
        f.write(p18_dtos.strip())
        
    # 4. Platform 18 Core Plugin
    p18_plugins = os.path.join(repo_root, "Backend", "Platform18", "plugins")
    os.makedirs(p18_plugins, exist_ok=True)
    
    p18_core = """
from Backend.Platform18.contracts.dtos import ExplainabilityReportDTO, VisualizationRequestDTO
from Backend.Platform10.contracts.dtos import MethodologyResultDTO
from Backend.shared_domain.contracts.dtos import LineageDTO, ConfidenceProfileDTO

class ExplainabilityCore:
    def __init__(self):
        self.registry = self._load_registry()
        
    def _load_registry(self):
        # In a real environment, this loads explainability_registry.yaml
        return {
            "adjusted_confidence": "Confidence after penalties and supporting evidence were applied."
        }
        
    def generate_report(self, methodology_results: list[MethodologyResultDTO]) -> ExplainabilityReportDTO:
        # Mock logic to prove Platform 18 operates on P10 artifacts
        
        supporting_text = []
        visualizations = []
        
        for res in methodology_results:
            prof = res.metadata.get("profile")
            if prof and prof.lineage:
                semantic_trace = prof.lineage.semantic.reasoning
                supporting_text.append(f"{res.methodology_id}: {semantic_trace}")
                
                if res.methodology_id == "p10_volume_profile":
                    visualizations.append(VisualizationRequestDTO(
                        visualization_type="Volume Profile",
                        data_source="VolumeProfileProfileDTO",
                        time_range_start="T-5",
                        time_range_end="T0",
                        highlighted_entities=["POC", "VAH"],
                        priority="High",
                        purpose="Support evidence for recommendation"
                    ))
                    
        report = ExplainabilityReportDTO(
            report_id="RPT-100",
            execution_timestamp="2026-07-07",
            target_recommendation_id=None,
            executive_summary="The market is currently showing mixed signals with a slight bullish bias based on macro data.",
            decision_summary="Proceed with caution, maintaining reduced exposure.",
            evidence_summary="Macro is dovish, but order flow shows short-term absorption.",
            supporting_evidence=supporting_text,
            conflicting_evidence=["Order Flow: Passive sellers absorbing initiative buyers."],
            confidence_analysis="High confidence from Macro, but low freshness from Trend.",
            freshness_analysis="All signals are fresh; Macro updated today.",
            risk_summary="Exposure limits are well within bounds.",
            lineage_summary="All signals traced deterministically to raw geometries.",
            methodology_contributions={"Macro": "Strong Bullish", "Order Flow": "Neutral/Bearish"},
            recommendations_for_further_review=["Check upcoming CPI print."],
            visualization_requests=visualizations
        )
        return report
"""
    with open(os.path.join(p18_plugins, "explainability_core.py"), "w") as f:
        f.write(p18_core.strip())
        
    # 5. Platform 18 Tests
    test_dir = os.path.join(repo_root, "Backend", "tests", "platform18")
    os.makedirs(test_dir, exist_ok=True)
    
    test_content = """
import unittest
from Backend.Platform18.plugins.explainability_core import ExplainabilityCore
from Backend.Platform10.contracts.dtos import MethodologyResultDTO, MarketStateDTO, ExecutionContext
from Backend.shared_domain.contracts.dtos import LineageDTO, SemanticTraceDTO, RuntimeTraceDTO

# A mock profile object to simulate P10 output
class MockProfile:
    def __init__(self):
        self.lineage = LineageDTO(
            runtime=RuntimeTraceDTO([], "", [], [], [], "", "", ""),
            semantic=SemanticTraceDTO(["CPI_Feature"], "Inflation data cooled.")
        )

class TestExplainabilityCore(unittest.TestCase):
    def test_report_generation(self):
        core = ExplainabilityCore()
        
        ctx = ExecutionContext("2026-07-07", "TEST", "R1")
        
        # Mock P10 Result
        res1 = MethodologyResultDTO(
            methodology_id="p10_macro",
            version="1.0", plugin_id="MacroCore", execution_id="R1", execution_context=ctx,
            score=0.8, confidence=0.8, strength=0.8, evidence=None, supporting_concepts=[],
            conflicting_concepts=[], preconditions=[], failure_reasons=[], explainability=None,
            metadata={"profile": MockProfile()}, execution_duration_ms=10, validation_status="VALID"
        )
        
        report = core.generate_report([res1])
        
        self.assertIsNotNone(report)
        self.assertIn("p10_macro: Inflation data cooled.", report.supporting_evidence)
        self.assertEqual(report.executive_summary, "The market is currently showing mixed signals with a slight bullish bias based on macro data.")

if __name__ == '__main__':
    unittest.main()
"""
    with open(os.path.join(test_dir, "test_explainability.py"), "w") as f:
        f.write(test_content.strip())
        
    print("Decision Intelligence Manifest, Explainability Registry, and Platform 18 Scaffolded.")

if __name__ == "__main__":
    repo = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
    scaffold_platform18_and_manifests(repo)
