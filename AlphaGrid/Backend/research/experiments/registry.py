"""Research Registry — Permanent scientific record of every experiment.

Stores successes AND failures to prevent repeating failed work and to
maintain a complete audit trail of AlphaGrid's research history.

Thread-safe. Serializable to JSON for persistence.
"""

import json
import logging
import threading
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ExperimentStatus(Enum):
    """Lifecycle states for a research experiment."""
    ACTIVE = "Active"
    COMPLETED = "Completed"
    ARCHIVED = "Archived"
    REJECTED = "Rejected"
    PROMOTED = "Promoted"


class ExperimentRecord:
    """A single record in the Research Registry."""

    __slots__ = ("experiment_id", "config", "status", "metrics",
                 "created_at", "updated_at", "notes")

    def __init__(
        self,
        experiment_id: str,
        config: Any,
        status: ExperimentStatus,
        metrics: Dict[str, float],
        notes: str = "",
    ) -> None:
        self.experiment_id = experiment_id
        self.config = config
        self.status = status
        self.metrics = metrics
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = self.created_at
        self.notes = notes

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the record to a JSON-compatible dictionary."""
        return {
            "experiment_id": self.experiment_id,
            "config": str(self.config),
            "status": self.status.value,
            "metrics": self.metrics,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "notes": self.notes,
        }


class ResearchRegistry:
    """
    Permanent scientific record of every experiment.
    Stores Active, Completed, Archived, Rejected, and Promoted outcomes.
    Thread-safe for concurrent experiment logging.
    """

    def __init__(self) -> None:
        self._records: Dict[str, ExperimentRecord] = {}
        self._lock = threading.Lock()

    def log_experiment(
        self,
        experiment_id: str,
        config: Any,
        status: ExperimentStatus,
        metrics: Dict[str, float],
        notes: str = "",
    ) -> None:
        """
        Logs an experiment outcome to the permanent record.

        Args:
            experiment_id: Unique identifier for the experiment.
            config: The ExperimentConfig or dict used for the run.
            status: The lifecycle status of the experiment.
            metrics: Dictionary of evaluation metrics (e.g., sharpe, max_drawdown).
            notes: Optional free-text notes.

        Raises:
            ValueError: If experiment_id is empty or already exists.
            ValueError: If metrics contain NaN or Inf values.
        """
        if not experiment_id:
            raise ValueError("experiment_id must not be empty")

        for key, value in metrics.items():
            if isinstance(value, float):
                if value != value:  # NaN check
                    raise ValueError(f"Metric '{key}' is NaN — invalid for research record")
                if value == float("inf") or value == float("-inf"):
                    raise ValueError(f"Metric '{key}' is Inf — invalid for research record")

        with self._lock:
            if experiment_id in self._records:
                raise ValueError(
                    f"Experiment '{experiment_id}' already exists in the registry. "
                    f"Use update_status() to modify existing experiments."
                )
            record = ExperimentRecord(
                experiment_id=experiment_id,
                config=config,
                status=status,
                metrics=metrics,
                notes=notes,
            )
            self._records[experiment_id] = record
            logger.info(
                "Logged experiment '%s' with status '%s'",
                experiment_id,
                status.value,
            )

    def update_status(
        self,
        experiment_id: str,
        new_status: ExperimentStatus,
        notes: str = "",
    ) -> None:
        """
        Transitions an experiment to a new lifecycle status.

        Args:
            experiment_id: The experiment to update.
            new_status: The new status.
            notes: Optional notes about why the status changed.

        Raises:
            ValueError: If experiment_id is not found.
        """
        with self._lock:
            if experiment_id not in self._records:
                raise ValueError(f"Experiment '{experiment_id}' not found in registry")
            record = self._records[experiment_id]
            record.status = new_status
            record.updated_at = datetime.now(timezone.utc)
            if notes:
                record.notes = notes

    def get_record(self, experiment_id: str) -> Dict[str, Any]:
        """
        Retrieves a single experiment record.

        Returns:
            Dictionary representation of the record, or empty dict if not found.
        """
        with self._lock:
            record = self._records.get(experiment_id)
            if record is None:
                return {}
            return record.to_dict()

    def get_by_status(self, status: ExperimentStatus) -> List[Dict[str, Any]]:
        """Returns all experiments matching the given status."""
        with self._lock:
            return [
                r.to_dict()
                for r in self._records.values()
                if r.status == status
            ]

    def get_all(self) -> List[Dict[str, Any]]:
        """Returns all experiment records."""
        with self._lock:
            return [r.to_dict() for r in self._records.values()]

    def count_by_status(self) -> Dict[str, int]:
        """Returns a count of experiments grouped by status."""
        with self._lock:
            counts: Dict[str, int] = {}
            for r in self._records.values():
                key = r.status.value
                counts[key] = counts.get(key, 0) + 1
            return counts

    def __len__(self) -> int:
        """Returns total number of experiments in the registry."""
        with self._lock:
            return len(self._records)

    def to_json(self) -> str:
        """Serializes the entire registry to a JSON string."""
        with self._lock:
            records_list = [r.to_dict() for r in self._records.values()]
            return json.dumps(records_list, indent=2, sort_keys=True)

    @classmethod
    def from_json(cls, json_str: str) -> "ResearchRegistry":
        """Deserializes a registry from a JSON string."""
        registry = cls()
        records_list = json.loads(json_str)
        for entry in records_list:
            status = ExperimentStatus(entry["status"])
            registry.log_experiment(
                experiment_id=entry["experiment_id"],
                config=entry.get("config", ""),
                status=status,
                metrics=entry.get("metrics", {}),
                notes=entry.get("notes", ""),
            )
        return registry
