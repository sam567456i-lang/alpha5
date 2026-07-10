from typing import List, Dict, Any

class LiquidityLevelEvidence:
    def __init__(self, bar_index: int, probability: float):
        self.bar_index = bar_index
        self.probability = probability

class LiquidityLevelRule:
    """
    Phase 3 Hypothesis Rule.
    Purely declarative. Instantiation of measurements must happen externally.
    """
    
    # Declarative dependencies
    CONSUMES = [
        {"measurement_type": "Pivot", "algorithm_id": "CENTERED_N_BAR", "config_keys": ["lookback", "lookforward"]},
    ]
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def evaluate(self, platform10_objects: Dict[str, List[Any]]) -> List[LiquidityLevelEvidence]:
        """
        Receives pre-computed arrays of Platform 10 objects.
        """
        pivots = platform10_objects.get("CenteredPivot", [])
        
        evidence = []
        for pivot in pivots:
            if pivot is None:
                continue
                
            # Naive hypothesis: every pivot is a liquidity level
            evidence.append(LiquidityLevelEvidence(
                bar_index=pivot["formation_bar"],
                probability=1.0
            ))
            
        return evidence
