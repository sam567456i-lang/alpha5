import time
import tracemalloc
from typing import List, Dict, Type
from Backend.core.methodologies.rules.base import BaseEvidenceRule
from Backend.core.methodologies.core_models import MethodologyContext

class RuleBenchmarkSuite:
    """Performance contract testing for atomic rules."""
    
    @staticmethod
    def run_benchmark(rule: BaseEvidenceRule, context: MethodologyContext, iterations: int = 1000) -> Dict[str, float]:
        latencies = []
        
        tracemalloc.start()
        for _ in range(iterations):
            start = time.perf_counter()
            rule.evaluate(context)
            end = time.perf_counter()
            latencies.append((end - start) * 1000) # milliseconds
            
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        latencies.sort()
        avg_latency = sum(latencies) / len(latencies)
        p95_latency = latencies[int(len(latencies) * 0.95)]
        p99_latency = latencies[int(len(latencies) * 0.99)]
        
        return {
            "rule_name": rule.name,
            "rule_version": str(rule.version),
            "iterations": float(iterations),
            "avg_latency_ms": avg_latency,
            "p95_latency_ms": p95_latency,
            "p99_latency_ms": p99_latency,
            "peak_memory_kb": peak / 1024,
            "throughput_hz": 1000.0 / avg_latency if avg_latency > 0 else float('inf')
        }
