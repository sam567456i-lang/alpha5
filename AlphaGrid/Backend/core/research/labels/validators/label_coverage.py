from typing import List
from Backend.core.research.labels.label import Label

class LabelCoverageValidator:
    """
    Validates the macro distribution of labels across a dataset to detect
    coverage drift (e.g. suddenly 38% Positive when historically 2.3%).
    """
    
    @staticmethod
    def validate_coverage(labels: List[Label], expected_positive_max: float = 0.10) -> bool:
        total = len(labels)
        if total == 0:
            return False
            
        positives = sum(1 for l in labels if l.derived_class == "POSITIVE")
        negatives = sum(1 for l in labels if l.derived_class == "NEGATIVE")
        neutrals = sum(1 for l in labels if l.derived_class == "NEUTRAL")
        
        pos_ratio = positives / total
        neg_ratio = negatives / total
        neu_ratio = neutrals / total
        
        print(f"Coverage Report: Positive {pos_ratio*100:.1f}% | Negative {neg_ratio*100:.1f}% | Neutral {neu_ratio*100:.1f}%")
        
        if pos_ratio > expected_positive_max:
            print(f"WARNING: Positive coverage drift detected ({pos_ratio*100:.1f}% > {expected_positive_max*100:.1f}%)")
            return False
            
        return True
