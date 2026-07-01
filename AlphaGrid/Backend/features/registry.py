"""Feature Registry and Dependency DAG Builder."""

from typing import Type, Dict, List, Set
from .base import AbstractFeature


class FeatureRegistry:
    """
    Registers AbstractFeature implementations and resolves their dependency DAG.
    Ensures shared prerequisites are only computed once.
    """

    def __init__(self) -> None:
        self._features: Dict[str, Type[AbstractFeature]] = {}
        self._ordered_features: List[str] = []

    def register(self, feature_cls: Type[AbstractFeature]) -> None:
        """Registers a feature class."""
        if not issubclass(feature_cls, AbstractFeature):
            raise TypeError(f"Feature {feature_cls.__name__} must inherit from AbstractFeature")
        
        name = feature_cls.get_name()
        if name in self._features:
            raise ValueError(f"Duplicate feature name: '{name}'")
            
        self._features[name] = feature_cls
        # Invalidate ordered cache
        self._ordered_features = []

    def build_dag(self) -> List[Type[AbstractFeature]]:
        """
        Builds and returns a topological ordering of registered features.
        Raises ValueError if there are missing dependencies or circular dependencies.
        """
        if self._ordered_features:
            return [self._features[name] for name in self._ordered_features]

        # 1. Check for missing dependencies
        for name, cls in self._features.items():
            for dep in cls.get_dependencies():
                if dep not in self._features:
                    raise ValueError(f"Feature '{name}' depends on '{dep}', which is not registered.")

        # 2. Topological Sort (Kahn's Algorithm or DFS)
        # Using DFS for cycle detection
        visited: Set[str] = set()
        temp_marked: Set[str] = set()
        ordered: List[str] = []

        def visit(n: str) -> None:
            if n in temp_marked:
                raise ValueError(f"Circular dependency detected involving feature '{n}'")
            if n not in visited:
                temp_marked.add(n)
                cls = self._features[n]
                for dep in cls.get_dependencies():
                    visit(dep)
                temp_marked.remove(n)
                visited.add(n)
                ordered.append(n)

        for name in self._features:
            if name not in visited:
                visit(name)

        self._ordered_features = ordered
        return [self._features[name] for name in self._ordered_features]

    def get_feature(self, name: str) -> Type[AbstractFeature]:
        """Retrieves a single feature class by name."""
        if name not in self._features:
            raise ValueError(f"Feature '{name}' is not registered.")
        return self._features[name]

    def get_all_names(self) -> List[str]:
        """Returns a list of all registered feature names."""
        return list(self._features.keys())

    def get_max_warmup(self) -> int:
        """Returns the maximum warmup period across all registered features."""
        if not self._features:
            return 0
        return max(cls.warmup_period() for cls in self._features.values())

    def clear(self) -> None:
        """Clears the registry (useful for testing)."""
        self._features.clear()
        self._ordered_features.clear()

    def __len__(self) -> int:
        """Returns the number of registered features."""
        return len(self._features)
