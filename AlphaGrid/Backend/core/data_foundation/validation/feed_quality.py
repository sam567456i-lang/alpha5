from typing import Iterator, List, Dict, Any, Tuple
from datetime import datetime, timedelta
from Backend.core.data_foundation.contracts.schemas import (
    OHLCSchema, ValidationProfile, FeedQualityReport, QualityScore, GapPolicy, DuplicatePolicy
)
from Backend.core.data_foundation.registry.market_registry import MarketMetadata

class FeedQualityEngine:
    """Computes multidimensional data quality scores based on strict validation exceptions."""
    
    def __init__(self, dataset_id: str, profile: ValidationProfile, market_metadata: MarketMetadata, resolution_td: timedelta):
        self.dataset_id = dataset_id
        self.profile = profile
        self.market_metadata = market_metadata
        self.resolution_td = resolution_td
        
        self.errors = []
        self.warnings = []
        self.repairs_applied = 0
        
        # Scoring metrics
        self.total_processed = 0
        self.duplicate_count = 0
        self.integrity_failures = 0
        self.chronology_failures = 0
        self.calendar_failures = 0
        self.gap_count = 0
        self.normalization_failures = 0

    def validate_stream(self, stream: Iterator[OHLCSchema]) -> Tuple[Iterator[OHLCSchema], FeedQualityReport]:
        """Consumes an iterator of normalized bars, applies validation, and yields valid/repaired bars."""
        
        last_ts = None
        
        def _generator():
            nonlocal last_ts
            for bar in stream:
                self.total_processed += 1
                is_valid = True
                
                # 1. Duplicates
                if last_ts and bar.timestamp == last_ts:
                    self.duplicate_count += 1
                    if self.profile.duplicate_policy == DuplicatePolicy.FAIL:
                        self.errors.append(f"Duplicate timestamp detected at {bar.timestamp}")
                        is_valid = False
                    elif self.profile.duplicate_policy == DuplicatePolicy.WARN:
                        self.warnings.append(f"Duplicate timestamp ignored at {bar.timestamp}")
                        continue
                    else: # REPAIR
                        self.repairs_applied += 1
                        continue # simple repair: drop duplicate
                
                # 2. Chronology
                if last_ts and bar.timestamp < last_ts:
                    self.chronology_failures += 1
                    self.errors.append(f"Chronology violation: {bar.timestamp} before {last_ts}")
                    is_valid = False
                    
                # 3. Gaps & Resolution Consistency
                if last_ts and bar.timestamp > last_ts:
                    expected_next = last_ts + self.resolution_td
                    if bar.timestamp > expected_next:
                        # (Basic gap detection. In real-world, we'd check against calendar to see if gap is a weekend)
                        self.gap_count += 1
                        if self.profile.gap_policy == GapPolicy.FAIL:
                            self.errors.append(f"Gap detected between {last_ts} and {bar.timestamp}")
                            is_valid = False
                        elif self.profile.gap_policy == GapPolicy.WARN:
                            self.warnings.append(f"Gap detected between {last_ts} and {bar.timestamp}")
                        elif self.profile.gap_policy == GapPolicy.REPAIR:
                            self.repairs_applied += 1
                            # Synthetic repair would insert bars here. (Mocked for now)

                # 4. Integrity (Negative values, Impossible OHLC)
                if bar.open < 0 or bar.high < 0 or bar.low < 0 or bar.close < 0 or bar.volume < 0:
                    self.integrity_failures += 1
                    self.errors.append(f"Negative price/volume at {bar.timestamp}")
                    is_valid = False
                    
                if bar.high < bar.low:
                    self.integrity_failures += 1
                    self.errors.append(f"High < Low at {bar.timestamp}")
                    is_valid = False
                    
                if not (bar.low <= bar.open <= bar.high) or not (bar.low <= bar.close <= bar.high):
                    self.integrity_failures += 1
                    self.errors.append(f"Open/Close outside High/Low bounds at {bar.timestamp}")
                    is_valid = False

                # 5. Calendar Consistency (Weekends/Holidays)
                if self.market_metadata.market_type.name != "CRYPTO":
                    if bar.timestamp.weekday() >= 5: # Saturday/Sunday
                        self.calendar_failures += 1
                        self.errors.append(f"Weekend bar detected in non-crypto market at {bar.timestamp}")
                        is_valid = False
                
                if is_valid:
                    last_ts = bar.timestamp
                    yield bar
                    
        validated_stream = _generator()
        return validated_stream, self # Note: In production, the report is generated AFTER iteration completes.
        
    def generate_report(self) -> FeedQualityReport:
        total = max(1, self.total_processed)
        
        completeness = max(0.0, 1.0 - (self.gap_count / total))
        consistency = max(0.0, 1.0 - (self.integrity_failures / total))
        integrity = max(0.0, 1.0 - (self.integrity_failures / total))
        chronology = max(0.0, 1.0 - (self.chronology_failures / total))
        calendar = max(0.0, 1.0 - (self.calendar_failures / total))
        duplicates = max(0.0, 1.0 - (self.duplicate_count / total))
        normalization = max(0.0, 1.0 - (self.normalization_failures / total))
        
        score = QualityScore(completeness, consistency, integrity, chronology, calendar, duplicates, normalization)
        
        status = "ACCEPTED"
        if len(self.errors) > 0:
            status = "REJECTED"
        elif self.repairs_applied > 0:
            status = "REPAIRED"
            
        return FeedQualityReport(
            dataset_id=self.dataset_id,
            validation_profile=self.profile.name,
            errors=self.errors,
            warnings=self.warnings,
            repairs_applied=self.repairs_applied,
            quality_score=score,
            status=status
        )
