import uuid
from typing import List, Dict, Any, Callable
from dataclasses import dataclass, field
from Backend.core.methodology.narrative_node import TradeSetupNode, FeatureVectorNode, ScoreResultNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage

@dataclass
class MethodologyScorePolicy:
    """
    Defines how extracted neutral features are weighted to produce a score.
    """
    methodology_name: str
    weights: Dict[str, float] = field(default_factory=dict)
    
    def compute_score(self, features: Dict[str, Any]) -> float:
        score = 0.0
        for feature_name, weight in self.weights.items():
            value = features.get(feature_name, 0)
            if isinstance(value, bool):
                score += weight if value else 0
            elif isinstance(value, (int, float)):
                score += weight * value
        return score
        
    def get_grade(self, score: float) -> str:
        if score >= 80: return "A"
        if score >= 60: return "B"
        if score >= 40: return "C"
        return "F"

class ScoringEngine:
    """
    Extracts neutral features from a TradeSetupNode and applies a MethodologyScorePolicy.
    """
    def __init__(self, extractors: Dict[str, Callable[[TradeSetupNode], Any]]):
        self.extractors = extractors
        
    def extract_features(self, setup: TradeSetupNode) -> FeatureVectorNode:
        features = {}
        for name, extractor in self.extractors.items():
            features[name] = extractor(setup)
            
        return FeatureVectorNode(
            node_id=f"fv_{uuid.uuid4().hex[:8]}",
            identity=None,
            concept_type=NarrativeNodeType.FEATURE_VECTOR,
            concept_name=f"Features for {setup.concept_name}",
            stage=NarrativeStage.SETUP,
            setup_id=setup.node_id,
            features=features
        )
        
    def score_setup(self, feature_vector: FeatureVectorNode, policy: MethodologyScorePolicy) -> ScoreResultNode:
        score = policy.compute_score(feature_vector.features)
        grade = policy.get_grade(score)
        
        return ScoreResultNode(
            node_id=f"score_{uuid.uuid4().hex[:8]}",
            identity=None,
            concept_type=NarrativeNodeType.FEATURE_VECTOR, # Score result lives in same conceptual area
            concept_name=f"Score for {feature_vector.setup_id}",
            stage=NarrativeStage.SETUP,
            setup_id=feature_vector.setup_id,
            score=score,
            grade=grade
        )
