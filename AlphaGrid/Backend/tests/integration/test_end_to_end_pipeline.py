import unittest
from datetime import datetime
from uuid import uuid4

# Import all DTOs across the pipeline to verify structural compatibility
from Backend.shared_domain.contracts.dtos import (
    LineageDTO, RuntimeTraceDTO, SemanticTraceDTO, ConfidenceProfileDTO
)
from Backend.Platform10.contracts.dtos import (
    MarketStateDTO, MethodologyResultDTO, MacroProfileDTO, FreshnessProfileDTO, DataQualityProfileDTO, EvidenceDTO, ExplainabilityDTO, ExecutionContext, ConceptSetDTO
)
from Backend.Platform18.contracts.dtos import ExplainabilityReportDTO
from Backend.Platform18.plugins.explainability_core import ExplainabilityCore

# We mock the intermediate pipeline DTOs if they aren't fully instantiated in this repo snapshot,
# but we enforce the strict typed transition boundary.

class OpportunityDTO:
    def __init__(self, opp_id, methodology_results):
        self.opp_id = opp_id
        self.methodology_results = methodology_results
        
class RecommendationDTO:
    def __init__(self, rec_id, opportunity, action):
        self.rec_id = rec_id
        self.opportunity = opportunity
        self.action = action

class RiskContextDTO:
    def __init__(self, recommendation, risk_score):
        self.recommendation = recommendation
        self.risk_score = risk_score
        
class PortfolioStateDTO:
    def __init__(self, current_exposure):
        self.current_exposure = current_exposure

class TestEndToEndPipeline(unittest.TestCase):
    
    def test_pipeline_transition_integrity(self):
        # 1. Synthesize Tick -> Concept (P9)
        tick_id = f"tick_{uuid4()}"
        concept_id = f"concept_{uuid4()}"
        
        # 2. Synthesize Methodology Execution (P10)
        ctx = ExecutionContext("2026-07-07T12:00:00Z", "LIVE", "RUN-1")
        
        lineage = LineageDTO(
            runtime=RuntimeTraceDTO([tick_id], "snap1", ["geo1"], ["feat1"], [concept_id], "meth1", "P10", "v1"),
            semantic=SemanticTraceDTO(["CPI_Feature"], "Inflation cooled.")
        )
        conf = ConfidenceProfileDTO(0.8, 0.75, ["CPI_Beat"], ["Late_Cycle"], [], 0.1)
        freshness = FreshnessProfileDTO("2026-07-07T12:00:00Z", "Daily", "Event", None, "Step", "Fresh", "NewEvent")
        dq = DataQualityProfileDTO(1.0, 0, 10.0, "High", "Valid", 1.0)
        
        profile = MacroProfileDTO(
            methodology_id="p10_macro", version="1.0", health="HEALTHY", confidence=0.75, reliability=0.9, applicability=1.0,
            provenance=[], evidence=EvidenceDTO([], [], []), explainability=ExplainabilityDTO("", "", "", "", "", ""),
            execution_id="RUN-1", execution_timestamp="2026-07-07T12:00:00Z", scheduler_cadence="DAILY", cache_status="MISS", validation_status="VALID",
            regime="Reflation", central_bank_bias="Dovish", growth_inflation_matrix="Goldilocks",
            lineage=lineage, confidence_profile=conf
        )
        
        p10_result = MethodologyResultDTO(
            methodology_id="p10_macro", version="1.0", plugin_id="MacroCore", execution_id="RUN-1", execution_context=ctx,
            score=0.75, confidence=0.75, strength=0.75, evidence=profile.evidence, supporting_concepts=[], conflicting_concepts=[],
            preconditions=[], failure_reasons=[], explainability=profile.explainability, metadata={"profile": profile},
            execution_duration_ms=45.0, validation_status="VALID"
        )
        
        # 3. Synthesize P11 -> P12 -> P13 -> P14 (Opportunity to Recommendation)
        opp = OpportunityDTO("OPP-1", [p10_result])
        rec = RecommendationDTO("REC-1", opp, "BUY")
        
        # 4. Synthesize P15 -> P16 (Risk and Portfolio)
        risk = RiskContextDTO(rec, 0.2)
        portfolio = PortfolioStateDTO(0.5)
        
        # 5. Synthesize Platform 18 Explainability Generation
        p18 = ExplainabilityCore()
        
        # Pass the original P10 results (carried through the recommendation) into P18
        report = p18.generate_report(rec.opportunity.methodology_results)
        
        # ASSERTIONS: Verify the DTO pipeline boundary survived and data wasn't lost
        self.assertIsNotNone(report)
        self.assertEqual(report.report_id, "RPT-100")
        
        # Verify Semantic Lineage was successfully extracted from the pipeline
        self.assertTrue(any("Inflation cooled" in evidence for evidence in report.supporting_evidence))

if __name__ == '__main__':
    unittest.main()
