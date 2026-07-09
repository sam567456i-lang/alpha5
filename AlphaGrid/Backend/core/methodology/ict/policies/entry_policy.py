from dataclasses import dataclass, field
from typing import List

@dataclass
class OTEPolicy:
    """Rules for identifying an Optimal Trade Entry."""
    min_fib_level: float = 0.618
    max_fib_level: float = 0.786
    requires_htf_alignment: bool = True
    required_confluence_count: int = 1

@dataclass
class FVGEntryPolicy:
    """Rules for entering off a Fair Value Gap."""
    requires_displacement: bool = True
    mitigation_threshold: float = 0.5 # Must hit at least 50% of the FVG
    requires_htf_alignment: bool = True

@dataclass
class ICTEntryPolicy:
    """
    Configurable ruleset for evaluating entry propositions (Candidates).
    """
    allowed_sessions: List[str] = field(default_factory=lambda: ["LONDON", "NEW_YORK"])
    ote: OTEPolicy = field(default_factory=OTEPolicy)
    fvg: FVGEntryPolicy = field(default_factory=FVGEntryPolicy)
