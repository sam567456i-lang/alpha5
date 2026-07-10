from typing import Dict, List

class FeatureGraph:
    """Compile-time verifiable directed acyclic graph (DAG) of features."""
    def __init__(self, edges: Dict[str, List[str]]):
        self.edges = edges # e.g. {"ATR": ["Rolling TR", "OHLC"]}

class FamilyDependencyGraph:
    """Compile-time verifiable directed acyclic graph (DAG) of analytical families."""
    def __init__(self, edges: Dict[str, List[str]]):
        self.edges = edges # e.g. {"Structure": ["Liquidity", "Time"]}
