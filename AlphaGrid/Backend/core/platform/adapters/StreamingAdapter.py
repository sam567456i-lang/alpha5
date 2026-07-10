from typing import List, Dict, Any
from Backend.core.platform.measurements.engine import MeasurementEngine, Causality

class StreamingAdapter:
    """
    Executes a MeasurementEngine in a causal, online fashion.
    Violently rejects OFFLINE engines to protect live trading integrity.
    """
    def __init__(self, engine: MeasurementEngine):
        if engine.causality == Causality.OFFLINE:
            raise ValueError(f"FATAL: Cannot run OFFLINE engine {engine.measurement_type} in StreamingAdapter.")
        self.engine = engine
        self.history = []
        
    def push(self, bar: Dict[str, Any]) -> Any:
        self.history.append(bar)
        current_idx = len(self.history) - 1
        return self.engine.step(self.history, current_idx)
