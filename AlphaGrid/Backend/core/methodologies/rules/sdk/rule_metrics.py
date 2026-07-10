import numpy as np
from typing import List

class RuleMetricsTracker:
    """Collects raw empirical performance statistics for a specific rule."""
    
    def __init__(self):
        self.latencies_ms: List[float] = []
        
    def log_latency(self, latency: float):
        self.latencies_ms.append(latency)
        
    def get_report(self) -> dict:
        if not self.latencies_ms:
            return {}
        
        arr = np.array(self.latencies_ms)
        return {
            "p50_latency_ms": np.percentile(arr, 50),
            "p95_latency_ms": np.percentile(arr, 95),
            "p99_latency_ms": np.percentile(arr, 99),
            "throughput_hz": 1000.0 / np.mean(arr) if np.mean(arr) > 0 else 0,
            "total_executions": len(arr)
        }
