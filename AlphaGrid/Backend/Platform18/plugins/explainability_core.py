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