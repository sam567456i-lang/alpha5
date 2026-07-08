from dataclasses import dataclass

@dataclass(frozen=True)
class EvidenceIdentityDTO:
    """The unique identity of a specific piece of evidence."""
    evidence_id: str
    evidence_type: str
    capability_id: str
    ontology_id: str
