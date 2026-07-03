"""Dependency Injection registry hook for the Evidence domain."""

from Backend.foundation.dependency_injection_container import DependencyContainer
from Backend.evidence.engine import EvidenceEngine

def register_evidence(container: DependencyContainer) -> None:
    """
    Registers the Evidence domain components into the DI container.
    """
    container.register_factory("evidence_engine", lambda c: EvidenceEngine(), singleton=True)
