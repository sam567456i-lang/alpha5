"""In-memory repository implementation for Research Platform tests."""

from typing import Dict, List, Optional
from uuid import UUID
import threading
from Backend.research.models.dataset import DatasetSnapshot
from Backend.research.models.experiment import Experiment
from Backend.research.models.result import BacktestResult
from .interfaces import IExperimentRepository, IDatasetSnapshotRepository


class MemoryExperimentRepository(IExperimentRepository):
    """Thread-safe in-memory experiment repository."""

    def __init__(self) -> None:
        self._experiments: Dict[UUID, Experiment] = {}
        self._results: Dict[UUID, BacktestResult] = {}
        self._lock = threading.Lock()

    def save_experiment(self, experiment: Experiment) -> None:
        """Saves a single experiment."""
        with self._lock:
            self._experiments[experiment.id] = experiment

    def get_experiment(self, experiment_id: UUID) -> Optional[Experiment]:
        """Retrieves an experiment by ID."""
        with self._lock:
            return self._experiments.get(experiment_id)

    def list_experiments(self) -> List[Experiment]:
        """Lists all stored experiments."""
        with self._lock:
            return list(self._experiments.values())

    def archive_experiment_with_result(self, experiment: Experiment, result: BacktestResult) -> None:
        """Atomically saves an archived experiment and its backtest result."""
        if not experiment.is_archived:
            raise ValueError("Experiment must be archived to use this method.")
        if experiment.id != result.experiment_id:
            raise ValueError("Result experiment_id does not match experiment.id")

        with self._lock:
            self._experiments[experiment.id] = experiment
            self._results[experiment.id] = result

    def get_result(self, experiment_id: UUID) -> Optional[BacktestResult]:
        """Retrieves the result for an experiment (test helper)."""
        with self._lock:
            return self._results.get(experiment_id)


class MemoryDatasetSnapshotRepository(IDatasetSnapshotRepository):
    """Thread-safe in-memory dataset snapshot repository."""

    def __init__(self) -> None:
        self._snapshots: Dict[str, DatasetSnapshot] = {}
        self._lock = threading.Lock()

    def save_snapshot(self, snapshot: DatasetSnapshot) -> None:
        """Saves a dataset snapshot."""
        with self._lock:
            self._snapshots[snapshot.snapshot_id] = snapshot

    def get_snapshot(self, snapshot_id: str) -> Optional[DatasetSnapshot]:
        """Retrieves a dataset snapshot by its canonical hash."""
        with self._lock:
            return self._snapshots.get(snapshot_id)
