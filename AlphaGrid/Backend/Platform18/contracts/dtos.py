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