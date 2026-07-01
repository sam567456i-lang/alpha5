"""Candidate Strategy Registry — stores successfully promoted strategies.

Only strategies that pass Scientific Validation and Promotion Review
are persisted here, awaiting Paper Trading in later phases.

Thread-safe. Provides query and serialization capabilities.
"""

import json
import logging
import threading
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class CandidateStatus(Enum):
    """Lifecycle states for a candidate strategy."""
    PENDING_PAPER_TRADE = "PendingPaperTrade"
    PAPER_TRADING = "PaperTrading"
    APPROVED_LIVE = "ApprovedLive"
    RETIRED = "Retired"


class CandidateRecord:
    """A single record in the Candidate Registry."""

    __slots__ = ("strategy_id", "experiment_id", "config", "validation_metrics",
                 "status", "promoted_at", "notes")

    def __init__(
        self,
        strategy_id: str,
        experiment_id: str,
        config: Any,
        validation_metrics: Dict[str, float],
        notes: str = "",
    ) -> None:
        self.strategy_id = strategy_id
        self.experiment_id = experiment_id
        self.config = config
        self.validation_metrics = validation_metrics
        self.status = CandidateStatus.PENDING_PAPER_TRADE
        self.promoted_at = datetime.now(timezone.utc)
        self.notes = notes

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the record to a JSON-compatible dictionary."""
        return {
            "strategy_id": self.strategy_id,
            "experiment_id": self.experiment_id,
            "config": str(self.config),
            "validation_metrics": self.validation_metrics,
            "status": self.status.value,
            "promoted_at": self.promoted_at.isoformat(),
            "notes": self.notes,
        }


class CandidateRegistry:
    """
    Stores only successfully promoted strategies awaiting Paper Trading.
    Thread-safe for concurrent access.
    """

    def __init__(self) -> None:
        self._candidates: Dict[str, CandidateRecord] = {}
        self._lock = threading.Lock()

    def promote_candidate(
        self,
        strategy_id: str,
        experiment_id: str,
        config: Any,
        validation_metrics: Dict[str, float],
        notes: str = "",
    ) -> None:
        """
        Adds a promoted strategy to the registry.

        Args:
            strategy_id: Unique identifier for the candidate strategy.
            experiment_id: The experiment that validated this strategy.
            config: The strategy configuration that was validated.
            validation_metrics: Metrics from the validation phase.
            notes: Optional notes about the promotion.

        Raises:
            ValueError: If strategy_id is empty or already exists.
            ValueError: If validation_metrics contain NaN or Inf values.
        """
        if not strategy_id:
            raise ValueError("strategy_id must not be empty")
        if not experiment_id:
            raise ValueError("experiment_id must not be empty")

        for key, value in validation_metrics.items():
            if isinstance(value, float):
                if value != value:
                    raise ValueError(f"Metric '{key}' is NaN — invalid for candidate record")
                if value == float("inf") or value == float("-inf"):
                    raise ValueError(f"Metric '{key}' is Inf — invalid for candidate record")

        with self._lock:
            if strategy_id in self._candidates:
                raise ValueError(
                    f"Strategy '{strategy_id}' is already in the candidate registry"
                )
            record = CandidateRecord(
                strategy_id=strategy_id,
                experiment_id=experiment_id,
                config=config,
                validation_metrics=validation_metrics,
                notes=notes,
            )
            self._candidates[strategy_id] = record
            logger.info("Promoted strategy '%s' from experiment '%s'", strategy_id, experiment_id)

    def update_status(self, strategy_id: str, new_status: CandidateStatus) -> None:
        """Updates the lifecycle status of a candidate strategy."""
        with self._lock:
            if strategy_id not in self._candidates:
                raise ValueError(f"Strategy '{strategy_id}' not found in candidate registry")
            self._candidates[strategy_id].status = new_status

    def get_candidate(self, strategy_id: str) -> Dict[str, Any]:
        """Retrieves a single candidate record. Returns empty dict if not found."""
        with self._lock:
            record = self._candidates.get(strategy_id)
            if record is None:
                return {}
            return record.to_dict()

    def get_all_candidates(self) -> List[Dict[str, Any]]:
        """Returns all candidate records."""
        with self._lock:
            return [r.to_dict() for r in self._candidates.values()]

    def get_by_status(self, status: CandidateStatus) -> List[Dict[str, Any]]:
        """Returns all candidates matching the given status."""
        with self._lock:
            return [
                r.to_dict()
                for r in self._candidates.values()
                if r.status == status
            ]

    def __len__(self) -> int:
        """Returns total number of candidates."""
        with self._lock:
            return len(self._candidates)

    def to_json(self) -> str:
        """Serializes the entire registry to a JSON string."""
        with self._lock:
            records_list = [r.to_dict() for r in self._candidates.values()]
            return json.dumps(records_list, indent=2, sort_keys=True)
