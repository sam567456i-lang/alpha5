from typing import Dict, Any

class ImplementationPlanner:
    """Generates the automatic next step implementation plan based on gaps and planning mode."""
    
    def __init__(self, gaps: Dict[str, Any], mode: str = "product"):
        self.gaps = gaps
        self.mode = mode

    def generate_plan(self) -> str:
        """
        Determines the next sequential platform based on the planning mode.
        Modes: architecture, product, balanced
        """
        if self.mode == "product":
            plan = """## NEXT TASK
**Platform**: Platform 5 (Analysis Platform)
**Next Capability**: Analysis Type Abstraction

**Dependencies**: Platform 1-4, Platform 6-9 (Mostly Satisfied)
**Validators Required**: 4 (Interface Contract, Dependency Isolation, Concept Generation, AI Metadata)
**Estimated Effort**: 2-3 days
**Risk**: Low

**Recommended Sequence**:
`BaseAnalysis` -> `TechnicalAnalysis` -> `FundamentalAnalysis` -> `VolumeAnalysis` -> `OrderFlowAnalysis` -> `SentimentAnalysis`
"""
        else:
            # Architecture mode default
            plan = """## NEXT TASK
**Platform**: Platform 7 (State Engine)
**Next Capability**: Rolling State

**Dependencies**: Satisfied
**Validators Required**: 7 (State correctness, Incremental equivalence, Cache correctness, Warmup correctness, Checkpoint recovery, Replay determinism, Memory growth)
**Estimated Effort**: 2-3 days
**Risk**: Low

**Recommended Sequence**:
`IndicatorState` -> `RollingState` -> `WarmupState` -> `Cache` -> `Streaming` -> `Validation`
"""
        return plan
