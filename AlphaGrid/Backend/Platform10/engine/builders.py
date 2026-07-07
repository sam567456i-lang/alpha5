from typing import Dict, Any, List
from Backend.Platform10.contracts.dtos import ConfidenceFactorsDTO, EvidenceDTO, ExplainabilityDTO

class ConfidenceEngine:
    """Centralized Confidence Calculation Engine"""
    
    @staticmethod
    def calculate_confidence(factors: ConfidenceFactorsDTO, model: str) -> float:
        """Computes centralized confidence score based on multi-dimensional factors and the specified model."""
        factor_values = list(factors.factors.values())
        if not factor_values:
            return 0.0
            
        if model == "LinearDecay":
            # Just an example implementation of a central model
            return sum(factor_values) / len(factor_values)
        elif model == "Pessimistic":
            return min(factor_values)
        else:
            return max(factor_values) # Default optimistic

class EvidenceBuilder:
    """Centralized Evidence Builder"""
    
    @staticmethod
    def build_evidence(raw_data: Dict[str, Any]) -> EvidenceDTO:
        supporting = raw_data.get("supporting_concepts", [])
        conflicting = raw_data.get("conflicting_concepts", [])
        raw = raw_data.get("raw_evidence", [])
        
        return EvidenceDTO(
            supporting_concepts=supporting,
            conflicting_concepts=conflicting,
            raw_evidence=raw
        )

class ExplainabilityBuilder:
    """Centralized Explainability Engine"""
    
    @staticmethod
    def build_explainability(evidence: EvidenceDTO, raw_data: Dict[str, Any]) -> ExplainabilityDTO:
        is_applicable = raw_data.get("is_applicable", False)
        
        why_app = "Conditions met based on feature alignment." if is_applicable else "N/A"
        why_not = "N/A" if is_applicable else "Required structural alignment missing."
        
        return ExplainabilityDTO(
            why_applicable=why_app,
            why_not_applicable=why_not,
            supporting_evidence_summary=", ".join(evidence.supporting_concepts) if evidence.supporting_concepts else "None",
            conflicting_evidence_summary=", ".join(evidence.conflicting_concepts) if evidence.conflicting_concepts else "None",
            required_conditions=", ".join(raw_data.get("required_conditions", [])),
            invalidating_conditions=", ".join(raw_data.get("invalidating_conditions", []))
        )
