from enum import Enum

class NarrativeNodeType(Enum):
    """
    Types of subjective narratives that a methodology can construct.
    """
    MARKET_CONTEXT = "MARKET_CONTEXT"
    SESSION_CONTEXT = "SESSION_CONTEXT"
    BIAS = "BIAS"
    POI = "POI"
    LIQUIDITY_TARGET = "LIQUIDITY_TARGET"
    STRUCTURE_NARRATIVE = "STRUCTURE_NARRATIVE"
    SETUP = "SETUP"
    FEATURE_VECTOR = "FEATURE_VECTOR"
    DECISION = "DECISION"
    EXECUTION_PLAN = "EXECUTION_PLAN"
    POSITION = "POSITION"
    MANAGEMENT = "MANAGEMENT"
    EXIT = "EXIT"
    RISK_NARRATIVE = "RISK_NARRATIVE"
    EXECUTION = "EXECUTION"
    ENTRY = "ENTRY"
    INVALIDATION = "INVALIDATION"
    DISPLACEMENT = "DISPLACEMENT"
    ACCUMULATION = "ACCUMULATION"
    MANIPULATION = "MANIPULATION"
    DISTRIBUTION = "DISTRIBUTION"
    CONFLICT = "CONFLICT"
    NARRATIVE_SEQUENCE = "NARRATIVE_SEQUENCE"
    
class MethodologyType(Enum):
    """
    Supported methodology namespaces.
    """
    ICT = "ICT"
    SMC = "SMC"
    WYCKOFF = "WYCKOFF"
    CUSTOM = "CUSTOM"

class NarrativeStage(Enum):
    """
    Explicit lifecycle stages of a methodological narrative.
    Enforces a strict Directed Acyclic Graph (DAG) for execution.
    """
    CONTEXT = "CONTEXT"
    TARGETING = "TARGETING"
    STRUCTURE = "STRUCTURE"
    SETUP = "SETUP"
    EXECUTION = "EXECUTION"
    MANAGEMENT = "MANAGEMENT"
    EXIT = "EXIT"

