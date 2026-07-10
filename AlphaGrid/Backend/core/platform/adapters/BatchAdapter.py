from typing import List, Dict, Any
from Backend.core.platform.measurements.engine import MeasurementEngine, Causality

class BatchAdapter:
    """
    Executes a MeasurementEngine over a full historical dataset.
    Permits OFFLINE engines (like centered pivots).
    """
    def __init__(self, engine: MeasurementEngine):
        self.engine = engine
        
    def run_all(self, history: List[Dict[str, Any]]) -> List[Any]:
        results = []
        for i in range(len(history)):
            results.append(self.engine.step(history, i))
        return results
