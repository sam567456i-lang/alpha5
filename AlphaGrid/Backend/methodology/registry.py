"""Methodology Registry.

Centrally catalogs reusable methodologies, tracking their lifecycle status, 
compatible features, concepts, and experiment history.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


from Shared.enums.methodology_status import MethodologyStatus

class MethodologyMetadata(BaseModel):
    """Metadata tracking the lifecycle and capability of a methodology."""
    name: str
    status: MethodologyStatus = Field(default=MethodologyStatus.EXPERIMENTAL, description="Experimental, Validated, Deprecated")
    version: str = Field(default="1.0.0")
    uses_concepts: List[str] = Field(default_factory=list)
    compatible_features: List[str] = Field(default_factory=list)
    compatible_strategies: List[str] = Field(default_factory=list)
    supported_models: List[str] = Field(default_factory=list, description="List of AI/ML models supported")
    performance_summary: Dict[str, float] = Field(default_factory=dict, description="e.g., {'avg_sharpe': 1.2}")
    research_history: List[str] = Field(default_factory=list, description="List of Experiment IDs")


class MethodologyRegistry:
    """
    Central catalog for reusable methodologies.
    Used for governance and multi-factor strategy composition.
    """

    def __init__(self) -> None:
        self._catalog: Dict[str, MethodologyMetadata] = {}

    def register(self, metadata: MethodologyMetadata) -> None:
        """Registers a methodology's metadata."""
        if metadata.name in self._catalog:
            raise ValueError(f"Methodology '{metadata.name}' is already registered.")
        self._catalog[metadata.name] = metadata

    def get_metadata(self, name: str) -> Optional[MethodologyMetadata]:
        """Retrieves metadata for a specific methodology."""
        return self._catalog.get(name)

    def append_experiment(self, name: str, experiment_id: str) -> None:
        """Appends an experiment ID to the methodology's research history."""
        if name not in self._catalog:
            raise ValueError(f"Methodology '{name}' not found.")
        self._catalog[name].research_history.append(experiment_id)

    def promote_status(self, name: str, status: str) -> None:
        """Promotes or updates the lifecycle status of a methodology."""
        if name not in self._catalog:
            raise ValueError(f"Methodology '{name}' not found.")
        self._catalog[name].status = status  # type: ignore

    def get_all(self) -> List[MethodologyMetadata]:
        """Returns all registered methodologies."""
        return list(self._catalog.values())

    def clear(self) -> None:
        """Clears the registry (useful for testing)."""
        self._catalog.clear()

# Global registry instance
METHODOLOGY_REGISTRY = MethodologyRegistry()
