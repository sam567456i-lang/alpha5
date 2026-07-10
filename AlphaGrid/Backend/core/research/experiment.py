from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime
import uuid

@dataclass(frozen=True)
class ExperimentRun:
    """Immutable record of a reproducible experiment."""
    experiment_id: str
    dataset_id: str
    methodology_version: str
    rule_versions: Dict[str, str]
    platform_version: str
    random_seed: int
    configuration: Dict[str, Any]
    execution_timestamp: datetime
    metrics: Dict[str, float]

class ExperimentRegistry:
    """MLflow-style tracker for all quantitative experiments."""
    def __init__(self):
        self._history: List[ExperimentRun] = []
        
    def log_experiment(self, run: ExperimentRun):
        self._history.append(run)
        
    def get_best_run(self, metric: str = "sharpe_ratio") -> ExperimentRun:
        if not self._history:
            raise ValueError("No experiments logged.")
        return max(self._history, key=lambda x: x.metrics.get(metric, -1.0))

class ExperimentFramework:
    """Orchestrates an experiment run, binding Simulation and Bias Detection."""
    def __init__(self, registry: ExperimentRegistry):
        self.registry = registry
        
    def execute(self, dataset_id: str, methodology: Any, config: Dict[str, Any]) -> ExperimentRun:
        # 1. Bias Checks
        # 2. Simulation Execution
        # 3. Metrics Generation
        # Stub
        run = ExperimentRun(
            experiment_id=str(uuid.uuid4()),
            dataset_id=dataset_id,
            methodology_version="1.0",
            rule_versions={},
            platform_version="12.5.0",
            random_seed=42,
            configuration=config,
            execution_timestamp=datetime.now(),
            metrics={"win_rate": 0.55, "expectancy": 0.12}
        )
        self.registry.log_experiment(run)
        return run
