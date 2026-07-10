from dataclasses import dataclass

@dataclass(frozen=True)
class EvidenceQualityMetadata:
    """Standardized quality metadata attached to ALL evidence."""
    confidence: float         # 0.0 to 1.0 (Algorithm confidence)
    coverage: float           # 0.0 to 1.0 (Percentage of data required that was available)
    freshness: float          # Age of underlying data in ms
    latency: float            # Execution computation time in ms
    source_quality: float     # 0.0 to 1.0 (Data provider quality)
    sample_size: int          # N underlying datapoints used
    stability: float          # 0.0 to 1.0 (Consistency of reading over time)
