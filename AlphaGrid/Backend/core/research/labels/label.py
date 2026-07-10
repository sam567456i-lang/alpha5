from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class Label:
    """
    A strictly versioned, immutable ground truth classification with full provenance.
    Separates the Objective Observation (facts) from the Derived Classification (Positive/Negative).
    """
    label_id: str
    target_object_id: str  # e.g., the LiquidityLevel UUID
    
    # Provenance Metadata
    dataset_version: str
    dataset_hash: str
    configuration_hash: str
    schema_version: str
    generator_version: str
    policy_version: str
    generation_timestamp_ms: int
    generator_commit: str
    
    # Objective Observation (Facts)
    observed_facts: Dict[str, Any]
    
    # Derived Classification
    derived_class: str  # 'POSITIVE', 'NEGATIVE', 'NEUTRAL'
    confidence: float
    
    # Validation Constraints
    lookahead_window_bars: int
    reason: Optional[str] = None
