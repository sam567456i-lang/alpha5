import json
import logging
import os
import time

logger = logging.getLogger("RuntimeAuditor.PerformanceProfiler")

class PerformanceProfiler:
    """Tracks latency metrics vs baseline."""
    
    def __init__(self):
        self.metrics = {}
        self._starts = {}

    def start(self, task: str):
        self._starts[task] = time.perf_counter()

    def end(self, task: str):
        if task in self._starts:
            elapsed = time.perf_counter() - self._starts.pop(task)
            self.metrics[task] = elapsed

    def export(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "performance_regression.json"), "w") as f:
            json.dump(self.metrics, f, indent=2)

