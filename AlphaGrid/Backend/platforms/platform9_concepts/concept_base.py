"""
Platform 10: Concept Platform - Base DTOs and Enums
Enforces strict consumption of Platform 9 Features and provides human-readable mappings.
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from abc import ABC
import hashlib

from Backend.core.state import ExecutionContext
from Backend.platforms.platform9_concepts.feature_base import BaseFeature

from Backend.platforms.platform9_concepts.semantic_evidence import SemanticEvidence

class ConceptCategory(str, Enum):
    """Broad categorization of concepts for high-level UI filtering."""
    TREND = "TREND"
    REGIME = "REGIME"
    VOLATILITY = "VOLATILITY"
    MOMENTUM = "MOMENTUM"
    LIQUIDITY = "LIQUIDITY"
    STRUCTURE = "STRUCTURE"
    ANOMALY = "ANOMALY"
    SPATIAL = "SPATIAL"


class ConceptType(str, Enum):
    """Specific types of concepts within a category."""
    BULL_MARKET = "BULL_MARKET"
    BEAR_MARKET = "BEAR_MARKET"
    RANGING_MARKET = "RANGING_MARKET"
    BREAKOUT = "BREAKOUT"
    MEAN_REVERSION = "MEAN_REVERSION"
    LIQUIDITY_VOID = "LIQUIDITY_VOID"
    VOLATILITY_EXPANSION = "VOLATILITY_EXPANSION"
    TREND_EXHAUSTION = "TREND_EXHAUSTION"
    FAIR_VALUE_GAP = "FAIR_VALUE_GAP"
    ORDER_BLOCK = "ORDER_BLOCK"
    BREAKER_BLOCK = "BREAKER_BLOCK"


class ConceptSeverity(str, Enum):
    """Severity or importance of a concept."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True, eq=True)
class ConceptID:
    """Unique, hashable identifier for a specific concept instance."""
    category: ConceptCategory
    type: ConceptType
    capability_id: str = "N/A"
    ontology_id: str = "N/A"
    version: str = "1.0.0"
    concept_version: int = 1
    previous_version_id: Optional[str] = None
    root_concept_id: Optional[str] = None
    
    @property
    def id_string(self) -> str:
        return f"{self.type.value}-{self.capability_id}-{self.concept_version}"


@dataclass
class BaseConcept(ABC):
    """
    Abstract Base Concept.
    All concepts must inherit from this and be fully immutable once frozen.
    Platform 10 Purity Rule: Concepts ONLY consume BaseFeatures from Platform 9.
    """
    concept_id: ConceptID
    source_features: List[BaseFeature] = field(default_factory=list)
    semantic_evidence: Optional[SemanticEvidence] = None
    description: str = "Base Concept Description"
    severity: ConceptSeverity = ConceptSeverity.LOW
    confidence: float = 1.0  # 0.0 to 1.0
    context: ExecutionContext = field(default_factory=lambda: ExecutionContext(
        session_id="N/A", trace_id="N/A", correlation_id="N/A", instrument_id="N/A",
        environment="TEST", runtime_mode="TEST", exchange="N/A", provider="N/A",
        market="N/A", timezone="UTC", sequence_id=0, is_replay=False, build_version="1.0"
    ))
    status: str = "DETECTED"
    lineage_hash: Optional[str] = None
    fingerprint_hash: Optional[str] = None
    
    _is_frozen: bool = field(init=False, default=False, repr=False)

    def __post_init__(self):
        # Validate that all source features are indeed BaseFeature instances from Platform 9
        for f in self.source_features:
            if not isinstance(f, BaseFeature):
                raise TypeError(f"Concept {self.concept_id} received invalid source: {type(f)}. Must be BaseFeature.")
            # BaseFeature type check is sufficient for Platform 9 origin validation in this architecture.

    def freeze(self):
        """Freezes the concept, making it immutable and generating its lineage hash."""
        if self._is_frozen:
            return

        # Calculate lineage hash based on source features and evidence
        hasher = hashlib.sha256()
        for f in sorted(self.source_features, key=lambda x: str(x.feature_id) if hasattr(x, 'feature_id') else str(x)):
            if hasattr(f, 'lineage_hash') and f.lineage_hash:
                hasher.update(f.lineage_hash.encode('utf-8'))
            else:
                hasher.update(str(f).encode('utf-8'))
                
        if self.semantic_evidence:
            hasher.update(str(self.semantic_evidence).encode('utf-8'))
        
        hasher.update(str(self.concept_id).encode('utf-8'))
        object.__setattr__(self, 'lineage_hash', hasher.hexdigest())
        
        # Calculate fingerprint hash (ontology, capability, evidence, objects, semantic version)
        f_hasher = hashlib.sha256()
        f_hasher.update(self.concept_id.ontology_id.encode('utf-8'))
        f_hasher.update(self.concept_id.capability_id.encode('utf-8'))
        f_hasher.update(self.concept_id.version.encode('utf-8'))
        if self.semantic_evidence:
            f_hasher.update(self.semantic_evidence.evidence_id.encode('utf-8'))
        object.__setattr__(self, 'fingerprint_hash', f_hasher.hexdigest())
        
        object.__setattr__(self, '_is_frozen', True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_is_frozen", False) and name != "_is_frozen":
            raise TypeError("Cannot modify a frozen BaseConcept instance.")
        super().__setattr__(name, value)
