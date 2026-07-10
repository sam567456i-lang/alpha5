from abc import ABC, abstractmethod
from Backend.core.methodologies.rules.sdk.rule_context import RuleContext, RuleResult
from Backend.core.methodologies.rules.sdk.rule_evidence import RuleEvidence
import time

class BaseEvidenceRule(ABC):
    """The foundational interface that ALL atomic evidence rules must implement."""
    
    def __init__(self, rule_id: str, version: str):
        self.rule_id = rule_id
        self.version = version
        
    def evaluate(self, context: RuleContext) -> RuleResult:
        """Wrapper method that enforces standard latency tracking and error handling."""
        start_time = time.perf_counter()
        
        try:
            result = self._detect(context)
        except Exception as e:
            # Proper error boundary so one failing rule doesn't crash the simulation
            print(f"[RuleError] {self.rule_id} failed: {e}")
            result = RuleResult(did_trigger=False)
            
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        # Inject standard telemetry if a rule fired
        if result.did_trigger and result.evidence:
            result.evidence.latency_ms = elapsed_ms
            result.evidence.rule_id = self.rule_id
            result.evidence.rule_version = self.version
            
        return result
        
    @abstractmethod
    def _detect(self, context: RuleContext) -> RuleResult:
        """The specific mathematical detection logic to be implemented by child classes."""
        pass
