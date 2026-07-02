"""Evaluation Registry."""

import threading
from typing import Dict, List
from Backend.research.evaluation.report import ScientificEvaluationReport

class EvaluationRegistry:
    """
    Stores all ScientificEvaluationReports.
    Acts as the immutable audit trail for every evaluated experiment.
    """
    
    _reports: Dict[str, ScientificEvaluationReport] = {}
    _lock = threading.Lock()

    @classmethod
    def register(cls, report: ScientificEvaluationReport) -> None:
        """Log a new evaluation report."""
        with cls._lock:
            if report.experiment_id in cls._reports:
                raise ValueError(f"Report for experiment {report.experiment_id} already exists.")
            cls._reports[report.experiment_id] = report

    @classmethod
    def get(cls, experiment_id: str) -> ScientificEvaluationReport:
        with cls._lock:
            if experiment_id not in cls._reports:
                raise KeyError(f"No evaluation report found for {experiment_id}.")
            return cls._reports[experiment_id]

    @classmethod
    def get_all(cls) -> List[ScientificEvaluationReport]:
        with cls._lock:
            return list(cls._reports.values())
        
    @classmethod
    def clear(cls) -> None:
        with cls._lock:
            cls._reports.clear()
