from typing import List, Tuple, Any

class SpatialIndex:
    """
    R-Tree / Interval Tree stub for geometric overlap queries.
    Prevents O(n) scans across millions of market objects.
    """
    def __init__(self):
        self.intervals = [] # Placeholder for interval tree
        
    def insert(self, entity_id: str, low_price: float, high_price: float):
        self.intervals.append((low_price, high_price, entity_id))
        
    def query_overlap(self, low: float, high: float) -> List[str]:
        # Naive O(n) scan for stub; would be O(log n + m) in real IntervalTree
        results = []
        for l, h, eid in self.intervals:
            if max(l, low) <= min(h, high):
                results.append(eid)
        return results
