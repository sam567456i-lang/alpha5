from dataclasses import dataclass, field

@dataclass
class BOSPolicy:
    """Rules for identifying a Break of Structure (Continuation)."""
    requires_context_alignment: bool = True

@dataclass
class CHOCHPolicy:
    """Rules for identifying a Change of Character (Reversal)."""
    requires_context_alignment: bool = False
    requires_poi_mitigation: bool = True

@dataclass
class MSSPolicy:
    """Rules for identifying a Market Structure Shift."""
    requires_htf_liquidity_sweep: bool = True
    requires_displacement: bool = True
    requires_multi_timeframe_confirmation: bool = True

@dataclass
class ICTStructurePolicy:
    """
    Configurable ruleset for evaluating structural propositions (Candidates).
    """
    bos: BOSPolicy = field(default_factory=BOSPolicy)
    choch: CHOCHPolicy = field(default_factory=CHOCHPolicy)
    mss: MSSPolicy = field(default_factory=MSSPolicy)
