from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class FairValueGapConcept:
    direction: str # Bullish | Bearish
    top_price: float
    bottom_price: float
    is_mitigated: bool
    
@dataclass(frozen=True)
class OrderBlockConcept:
    direction: str
    top_price: float
    bottom_price: float
    is_mitigated: bool

@dataclass(frozen=True)
class LiquiditySweepConcept:
    pool_type: str # BSL | SSL
    sweep_price: float
    rejection_strength: float

@dataclass(frozen=True)
class MarketStructureShiftConcept:
    direction: str
    swing_point_broken: float
    displacement_volume: float
    
@dataclass(frozen=True)
class AccumulationConcept:
    start_time: str
    end_time: str
    volume_profile: str
    
@dataclass(frozen=True)
class DistributionConcept:
    start_time: str
    end_time: str
    volume_profile: str

# --- Wave 3 Order Flow Concepts ---
@dataclass(frozen=True)
class OrderFlowImbalanceConcept: pass
@dataclass(frozen=True)
class DeltaDivergenceConcept: pass
@dataclass(frozen=True)
class AbsorptionConcept: pass
@dataclass(frozen=True)
class ExhaustionConcept: pass
@dataclass(frozen=True)
class InitiativeActivityConcept: pass
@dataclass(frozen=True)
class ResponsiveActivityConcept: pass
@dataclass(frozen=True)
class AggressiveBuyingConcept: pass
@dataclass(frozen=True)
class AggressiveSellingConcept: pass
@dataclass(frozen=True)
class PassiveBuyingConcept: pass
@dataclass(frozen=True)
class PassiveSellingConcept: pass
@dataclass(frozen=True)
class IcebergDetectionConcept: pass
@dataclass(frozen=True)
class LiquidityConsumptionConcept: pass
@dataclass(frozen=True)
class LiquidityRefillConcept: pass
@dataclass(frozen=True)
class DeltaFlipConcept: pass
@dataclass(frozen=True)
class CumulativeDeltaTrendConcept: pass
@dataclass(frozen=True)
class FootprintClusterConcept: pass
@dataclass(frozen=True)
class VolumeSpikeConcept: pass
@dataclass(frozen=True)
class SweepConfirmationConcept: pass

# --- Wave 3 Volume Profile Concepts ---
@dataclass(frozen=True)
class VolumeNodeConcept: pass
@dataclass(frozen=True)
class ValueAreaConcept: pass
@dataclass(frozen=True)
class POCMigrationConcept: pass
@dataclass(frozen=True)
class NakedPOCConcept: pass
@dataclass(frozen=True)
class DevelopingPOCConcept: pass
@dataclass(frozen=True)
class CompositeProfileConcept: pass
@dataclass(frozen=True)
class SessionProfileConcept: pass
@dataclass(frozen=True)
class WeeklyProfileConcept: pass
@dataclass(frozen=True)
class MonthlyProfileConcept: pass
@dataclass(frozen=True)
class AcceptanceConcept: pass
@dataclass(frozen=True)
class RejectionConcept: pass
@dataclass(frozen=True)
class BalanceConcept: pass
@dataclass(frozen=True)
class ImbalanceConcept: pass
@dataclass(frozen=True)
class DistributionShapeConcept: pass
@dataclass(frozen=True)
class RotationConcept: pass
@dataclass(frozen=True)
class ProfileShiftConcept: pass
@dataclass(frozen=True)
class InitiativeAuctionConcept: pass
@dataclass(frozen=True)
class ResponsiveAuctionConcept: pass

from typing import Optional, Dict

@dataclass(frozen=True)
class ConceptRelationshipDTO:
    relationship_type: str # requires | enhances | weakens | confirms | invalidates | depends_on | derived_from | complementary_to | mutually_exclusive_with | precedes | follows
    target_concept_uuid: str
    strength: float
    
# --- Wave 4 Macro / Event Concepts ---
@dataclass(frozen=True)
class MacroEventConcept: pass
@dataclass(frozen=True)
class InterestRateShiftConcept: pass
@dataclass(frozen=True)
class EconomicSurpriseConcept: pass

# --- Wave 4 Options Flow Concepts ---
@dataclass(frozen=True)
class GammaExposureConcept: pass
@dataclass(frozen=True)
class VannaCharmConcept: pass
@dataclass(frozen=True)
class DarkPoolBlockConcept: pass

# --- Wave 4 Sentiment / ML Concepts ---
@dataclass(frozen=True)
class SentimentShiftConcept: pass
@dataclass(frozen=True)
class MLPredictionConcept: pass
@dataclass(frozen=True)
class StatArbDeviationConcept: pass
