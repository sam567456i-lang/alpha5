from dataclasses import dataclass
from typing import List, Dict, Any
from Backend.core.methodology.dto.base_interpretation import BaseInterpretation

@dataclass(frozen=True)
class DecisionFeature:
    """
    Normalized, numerical or categorical feature extracted from the InterpretationGraph.
    Used exclusively by Platform 12 for downstream execution decision scoring.
    """
    feature_name: str
    feature_value: float
    source_interpretation_id: str

@dataclass(frozen=True)
class DecisionFeatureVector:
    """
    A unified vector of features representing the current state of the InterpretationGraph,
    ready to be consumed by a DecisionPolicy (Platform 12).
    """
    timestamp: str
    features: List[DecisionFeature]
    
class DecisionFeatureExtractor:
    """
    Architectural Bridge between Platform 11 and Platform 12.
    Consumes the InterpretationGraph (Objective semantic state) and flattens it 
    into a DecisionFeatureVector for risk, sizing, and execution policies.
    
    This ensures Platform 12 remains methodology-agnostic and never duplicates
    state extraction logic.
    """
    def extract_features(self, interpretations: List[BaseInterpretation]) -> DecisionFeatureVector:
        features = []
        for interp in interpretations:
            # Mock extraction logic
            feat = DecisionFeature(
                feature_name=f"{type(interp).__name__}_active",
                feature_value=1.0,
                source_interpretation_id=getattr(interp.identity, "id", "unknown")
            )
            features.append(feat)
            
        return DecisionFeatureVector(
            timestamp="current",
            features=features
        )
