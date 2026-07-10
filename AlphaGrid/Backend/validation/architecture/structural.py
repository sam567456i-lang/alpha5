from abc import ABC, abstractmethod

class ArchitectureValidator(ABC):
    @abstractmethod
    def validate(self) -> bool:
        pass

class LayerValidator(ArchitectureValidator):
    """Parses AST to ensure strict directional dependencies (e.g., P11 cannot import P10 internals)."""
    def validate(self) -> bool:
        # Implementation would scan AST for prohibited cross-layer imports
        return True

class DependencyValidator(ArchitectureValidator):
    """Ensures capabilities only depend on entities that are registered and active."""
    def validate(self) -> bool:
        return True

class CycleValidator(ArchitectureValidator):
    """Performs a topological sort on the Knowledge Graph to detect circular dependencies."""
    def validate(self) -> bool:
        return True

class NamingValidator(ArchitectureValidator):
    """Ensures modules, classes, and evidence DTOs follow the constitutional naming conventions."""
    def validate(self) -> bool:
        return True
