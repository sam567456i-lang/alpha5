from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Type
from Backend.core.methodologies.rules.evidence import RuleEvidence
from Backend.core.methodologies.core_models import MethodologyContext

class RuleVersion:
    """Explicit versioning for historical determinism."""
    def __init__(self, major: int, minor: int):
        self.major = major
        self.minor = minor
        
    def __str__(self):
        return f"v{self.major}.{self.minor}"

class BaseEvidenceRule(ABC):
    """The atomic base rule that composes methodologies."""
    name: str = "BaseRule"
    version: RuleVersion = RuleVersion(1, 0)
    
    def __init__(self, dependencies: List['BaseEvidenceRule'] = None):
        self.dependencies = dependencies or []
        self._detect_cycles()
        
    def _detect_cycles(self):
        # A simple check to prevent recursive DAG cycles in rule injection
        visited = set()
        def visit(rule):
            if id(rule) in visited:
                raise RecursionError(f"Cycle detected in Rule DAG at {rule.name}")
            visited.add(id(rule))
            for dep in rule.dependencies:
                visit(dep)
        visit(self)
        
    @abstractmethod
    def evaluate(self, context: MethodologyContext) -> Optional[RuleEvidence]:
        """Evaluates the rule against the frozen context."""
        pass

class DeterministicRule(BaseEvidenceRule):
    """A rule that outputs strict objective truths (e.g., FVG Exists)."""
    @abstractmethod
    def evaluate(self, context: MethodologyContext) -> Optional[RuleEvidence]:
        pass

class ProbabilisticRule(BaseEvidenceRule):
    """A rule that outputs statistical inferences (e.g., Spring Likelihood)."""
    @abstractmethod
    def evaluate(self, context: MethodologyContext) -> Optional[RuleEvidence]:
        pass
