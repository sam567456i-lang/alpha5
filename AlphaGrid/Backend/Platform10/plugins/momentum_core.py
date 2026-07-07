from typing import Dict, Any, Tuple
from Backend.Platform10.contracts.interfaces import IMethodologyPlugin
from Backend.Platform10.contracts.dtos import MarketStateDTO, ConfidenceFactorsDTO, MomentumProfileDTO, ProvenanceDTO, EvidenceDTO, ExplainabilityDTO

class MomentumCoreMethodology(IMethodologyPlugin):
    """Wave 1: Institutional Core Momentum Methodology (Capability-Driven)"""
    
    @property
    def methodology_id(self) -> str:
        return "cap_meth_momentum_core"
        
    @property
    def version(self) -> str:
        return "1.0.0"
        
    @property
    def capability_family(self) -> str:
        return "momentum"

    def evaluate_factors(self, market_state: MarketStateDTO) -> Tuple[ConfidenceFactorsDTO, Dict[str, Any]]:
        features = market_state.features.features
        
        # 1. Methodology Health & Applicability
        health = "Ready"
        required = ["MomentumDirection", "MomentumVelocity", "MomentumAcceleration", "MomentumPersistence", "MomentumDivergence", "TrendState", "MarketRegime"]
        missing = [f for f in required if f not in features]
        applicability = 1.0
        if missing:
            health = "Partial" if len(missing) < 3 else "Degraded"
            applicability -= (len(missing) * 0.15)
            applicability = max(0.0, applicability)
            
        # Abstract Capability Consumption (Mock resolution for capability simulation)
        direction_val = features.get("MomentumDirection", 1.0)
        velocity_val = features.get("MomentumVelocity", 0.5)
        acceleration_val = features.get("MomentumAcceleration", 0.1)
        persistence_val = features.get("MomentumPersistence", 0.4)
        divergence_val = features.get("MomentumDivergence", 0.0) # 0=None, 1=BullReg, -1=BearReg, 2=BullHidden, -2=BearHidden
        regime = features.get("MarketRegime", 1.0) # 1=Trend, 0=Range
        
        is_applicable = True if applicability > 0.3 else False
        direction_enum = "Bullish" if direction_val > 0 else "Bearish" if direction_val < 0 else "Neutral"
        velocity_enum = "Extreme" if velocity_val > 0.8 else "Strong" if velocity_val > 0.5 else "Moderate" if velocity_val > 0.2 else "Weak"
        accel_enum = "Increasing" if acceleration_val > 0.1 else "Decreasing" if acceleration_val < -0.1 else "Stable"
        pers_enum = "High" if persistence_val > 0.7 else "Medium" if persistence_val > 0.3 else "Low"
        
        div_map = {0: "None", 1: "Bullish Regular", -1: "Bearish Regular", 2: "Bullish Hidden", -2: "Bearish Hidden"}
        divergence_enum = div_map.get(divergence_val, "None")
        
        # Calculate Exhaustion Risk based on Velocity + Acceleration + Divergence
        exhaustion_val = velocity_val - acceleration_val
        exhaustion_enum = "Critical" if (exhaustion_val > 0.8 and divergence_enum != "None") else "High" if exhaustion_val > 0.6 else "Medium" if exhaustion_val > 0.3 else "Low"
        
        # 2. Invalidation Conditions & Evidence
        invalidating_conditions = []
        conflicting = []
        supporting = []
        
        if regime == 0.0:
            conflicting.append("Ranging Regime")
        else:
            supporting.append("Trending Regime")
            
        if accel_enum == "Decreasing" and exhaustion_enum in ["High", "Critical"]:
            conflicting.append("Momentum Exhaustion")
            
        if direction_enum == "Bullish" and divergence_enum == "Bearish Regular":
            conflicting.append("Bearish Divergence (Warning)")
            
        if velocity_val < 0.1:
            invalidating_conditions.append("Momentum collapse")
            
        # 3. Reliability & Confidence Provenance
        # Reliability is based on the congruence of the data (e.g. no divergence contradiction)
        reliability = 1.0 if not conflicting else 0.6 if len(conflicting) == 1 else 0.3
        
        provenance = [
            ProvenanceDTO("Momentum Strength", 0.4, 0.4 * velocity_val, "Velocity analysis"),
            ProvenanceDTO("Momentum Quality", 0.2, 0.2 * (1.0 if accel_enum == "Increasing" else 0.5), "Acceleration impact"),
            ProvenanceDTO("Momentum Persistence", 0.2, 0.2 * persistence_val, "Historical persistence"),
            ProvenanceDTO("Regime Compatibility", 0.2, 0.2 * (1.0 if regime == 1.0 else 0.4), "Market context"),
        ]
        
        final_confidence = sum(p.contribution for p in provenance)
        
        # 4. Momentum Profile DTO
        profile = MomentumProfileDTO(
            methodology_id=self.methodology_id,
            version=self.version,
            health=health,
            confidence=final_confidence,
            reliability=reliability,
            applicability=applicability,
            provenance=provenance,
            evidence=EvidenceDTO(supporting_concepts=supporting, conflicting_concepts=conflicting, raw_evidence=[p.reason for p in provenance]),
            explainability=ExplainabilityDTO(
                why_applicable="Sufficient capabilities" if is_applicable else "Insufficient capabilities",
                why_not_applicable="" if is_applicable else "Missing required capabilities",
                supporting_evidence_summary="Strong momentum" if velocity_val > 0.5 else "Weak momentum",
                conflicting_evidence_summary="Exhaustion risk" if len(conflicting)>0 else "None",
                required_conditions="Minimum Velocity Threshold",
                invalidating_conditions=", ".join(invalidating_conditions)
            ),
            execution_id=market_state.context.run_id,
            execution_timestamp=market_state.context.timestamp,
            scheduler_cadence="Every Candle",
            cache_status="MISS",
            validation_status="PENDING",
            direction=direction_enum,
            velocity=velocity_enum,
            acceleration=accel_enum,
            persistence=pers_enum,
            exhaustion=exhaustion_enum,
            divergence=divergence_enum,
            regime_compatibility="Trending" if regime == 1.0 else "Ranging"
        )
        
        factors = ConfidenceFactorsDTO(factors={p.factor: p.contribution for p in provenance})
        
        # 5. Emit Raw Data metadata exactly as dictated by platform contract
        raw_data = {
            "is_applicable": is_applicable,
            "supporting_concepts": supporting,
            "conflicting_concepts": conflicting,
            "raw_evidence": [p.reason for p in provenance],
            "required_conditions": ["Minimum Velocity Threshold"],
            "invalidating_conditions": invalidating_conditions,
            
            # Embed structured metadata
            "Methodology Health": health,
            "Applicability Score": applicability,
            "Reliability Score": reliability,
            "MomentumProfile": profile,
            "Missing Dependencies": missing,
            "Scheduler Cadence": "Every Candle"
        }
        
        return factors, raw_data
