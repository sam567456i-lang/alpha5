from typing import List, Tuple, Any

class TemporalIndex:
    """
    Time-series index for extremely fast temporal slicing.
    """
    def __init__(self):
        self.timestamps = [] # Placeholder for sorted list / B-Tree
        
    def insert(self, entity_id: str, timestamp_ms: int):
        self.timestamps.append((timestamp_ms, entity_id))
        self.timestamps.sort(key=lambda x: x[0])
        
    def query_range(self, start_ms: int, end_ms: int) -> List[str]:
        # Naive scan for stub; would be O(log n) binary search in real index
        results = []
        for t, eid in self.timestamps:
            if start_ms <= t <= end_ms:
                results.append(eid)
            elif t > end_ms:
                break
        return results
