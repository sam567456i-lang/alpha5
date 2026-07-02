"""Experiment status enumerations."""

from enum import StrEnum

class ExperimentStatus(StrEnum):
    """Lifecycle states for a research experiment."""
    ACTIVE = "Active"
    COMPLETED = "Completed"
    ARCHIVED = "Archived"
    REJECTED = "Rejected"
    PROMOTED = "Promoted"
