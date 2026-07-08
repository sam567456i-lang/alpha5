from enum import Enum, auto

class EvidenceClassification(Enum):
    PRIMITIVE = "Primitive"
    DERIVED = "Derived"
    COMPOSITE = "Composite"
    METHODOLOGY = "Methodology"
    CONSENSUS = "Consensus"
