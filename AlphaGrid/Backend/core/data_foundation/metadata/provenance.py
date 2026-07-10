from dataclasses import dataclass
from typing import List, Optional
import hashlib

@dataclass(frozen=True)
class ProvenanceHashes:
    dataset_hash: str
    transformation_hash: str
    schema_hash: str
    quality_hash: str

class DataLineageDAG:
    """Tracks the exact parent/child dataset inheritance."""
    
    def __init__(self):
        self.nodes = {}
        self.edges = []
        
    def add_transformation(self, parent_dataset_id: str, child_dataset_id: str, transformation_type: str):
        self.edges.append({
            "from": parent_dataset_id,
            "to": child_dataset_id,
            "transformation": transformation_type
        })
        
    def generate_hashes(self, raw_data_signature: str, transformation_logic_signature: str) -> ProvenanceHashes:
        d_hash = hashlib.sha256(raw_data_signature.encode()).hexdigest()
        t_hash = hashlib.sha256(transformation_logic_signature.encode()).hexdigest()
        return ProvenanceHashes(
            dataset_hash=d_hash,
            transformation_hash=t_hash,
            schema_hash="v1.0",
            quality_hash="Q1"
        )
