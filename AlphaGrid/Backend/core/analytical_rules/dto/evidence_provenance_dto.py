from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class EvidenceProvenanceDTO:
    """Traces the lineage of this evidence."""
    producer_rule: str
    execution_mode: str
    execution_timestamp: str
    source_evidence_ids: List[str]
    market_dataset_id: str
