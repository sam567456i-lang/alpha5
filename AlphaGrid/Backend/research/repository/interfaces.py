"""Abstract interfaces for Research Platform persistence."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from Backend.research.models.dataset import DatasetSnapshot
from Backend.research.models.experiment import Experiment
from Backend.research.models.result import BacktestResult


class IExperimentRepository(ABC):
    """Abstract interface for storing and retrieving experiments."""

    @abstractmethod
    def save_experiment(self, experiment: Experiment) -> None:
        """Saves a single experiment. Does not include results."""
        pass

    @abstractmethod
    def get_experiment(self, experiment_id: UUID) -> Optional[Experiment]:
        """Retrieves an experiment by ID."""
        pass

    @abstractmethod
    def list_experiments(self) -> List[Experiment]:
        """Lists all stored experiments."""
        pass

    @abstractmethod
    def archive_experiment_with_result(self, experiment: Experiment, result: BacktestResult) -> None:
        """Atomically saves an archived experiment and its backtest result."""
        pass


class IDatasetSnapshotRepository(ABC):
    """Abstract interface for storing and retrieving dataset snapshots."""

    @abstractmethod
    def save_snapshot(self, snapshot: DatasetSnapshot) -> None:
        """Saves a dataset snapshot."""
        pass

    @abstractmethod
    def get_snapshot(self, snapshot_id: str) -> Optional[DatasetSnapshot]:
        """Retrieves a dataset snapshot by its canonical hash (snapshot_id)."""
        pass
