from typing import Dict, Any, Tuple
from Backend.Platform10.contracts.interfaces import IMethodologyPlugin
from Backend.Platform10.contracts.dtos import MarketStateDTO, ConfidenceFactorsDTO, MeanReversionProfileDTO, ProvenanceDTO, EvidenceDTO, ExplainabilityDTO

class MeanReversionCoreMethodology(IMethodologyPlugin):
    """Wave 1: Institutional Core Mean Reversion Methodology"""
    
    @property
    def methodology_id(self) -> str:
        return "cap_meth_mean_reversion_core"
        
    @property
    def version(self) -> str:
        return "1.0.0"
        
    @property
    def capability_family(self) -> str:
        return "mean_reversion"

    def evaluate_factors(self, market_state: MarketStateDTO) -> Tuple[ConfidenceFactorsDTO, Dict[str, Any]]:
        features = market_state.features.features
        
        # 1. Methodology Health & Applicability
        health = "Ready"
        required = ["ReferenceValueDeviation", "RejectionQuality", "LiquidityReaction", "VolatilityCompression", "TrendState", "MarketRegime"]
        missing = [f for f in required if f not in features]
        applicability = 1.0
        if missing:
            health = "Partial" if len(missing) < 3 else "Degraded"
            applicability -= (len(missing) * 0.15)
            applicability = max(0.0, applicability)
            
        # Abstract Capability Consumption
        deviation_val = features.get("ReferenceValueDeviation", 0.0) # -1.0 to 1.0
        rejection_val = features.get("RejectionQuality", 0.0) # 0.0 to 1.0
        liquidity_val = features.get("LiquidityReaction", 0.0) # 0.0 to 1.0
        volatility_val = features.get("VolatilityCompression", 0.0) # 0=Expanded, 1=Compressed
        regime = features.get("MarketRegime", 0.0) # 1=Trend, 0=Range, 0.5=Transition
        
        is_applicable = True if applicability > 0.3 else False
        
        # Determine State
        if deviation_val > 0.7:
            state_enum = "Overextended Bullish" # Meaning price is far above mean, ripe for bearish reversion
        elif deviation_val < -0.7:
            state_enum = "Overextended Bearish"
        else:
            state_enum = "Equilibrium"
            
        # Deviation Severity
        abs_dev = abs(deviation_val)
        severity_enum = "Unprecedented" if abs_dev > 0.95 else "Extreme" if abs_dev > 0.8 else "High" if abs_dev > 0.6 else "Normal"
        
        # Target Estimation (Placeholder abstract logic)
        reversion_target_enum = "Complete" if rejection_val > 0.8 else "Primary" if rejection_val > 0.5 else "Weak" if rejection_val > 0.2 else "Unknown"
        
        # Structural & Statistical Confidence
        statistical_confidence = abs_dev
        structural_confidence = (rejection_val + liquidity_val) / 2.0
        
        # Probabilities
        prob_initiation = (statistical_confidence * 0.4) + (structural_confidence * 0.6)
        prob_completion = prob_initiation * (1.0 if regime == 0.0 else 0.5) # Harder to complete in a trend
        prob_failure = 1.0 - prob_completion
        
        # Structural categorization
        if rejection_val > 0.6:
            structure_enum = "Rejection Formation"
        elif volatility_val > 0.7:
            structure_enum = "Consolidation"
        else:
            structure_enum = "No Evidence"
            
        # 2. Invalidation Conditions & Evidence
        invalidating_conditions = []
        failure_conditions = []
        conflicting = []
        supporting = []
        
        if regime == 1.0:
            conflicting.append("Trending Regime")
            failure_conditions.append("Trend acceleration")
        else:
            supporting.append("Ranging Regime")
            
        if volatility_val < 0.2:
            failure_conditions.append("Volatility expansion")
            
        if state_enum == "Equilibrium":
            invalidating_conditions.append("Market in equilibrium")
            
        # 3. Reliability & Confidence Provenance
        reliability = 1.0 if not conflicting else 0.7 if len(conflicting) == 1 else 0.4
        
        provenance = [
            ProvenanceDTO("Statistical Deviation", 0.4, 0.4 * statistical_confidence, "Deviation from reference value"),
            ProvenanceDTO("Structural Rejection", 0.4, 0.4 * structural_confidence, "Price action structure"),
            ProvenanceDTO("Regime Compatibility", 0.2, 0.2 * (1.0 if regime <= 0.5 else 0.3), "Market context"),
        ]
        
        final_confidence = sum(p.contribution for p in provenance)
        
        # 4. Profile DTO
        profile = MeanReversionProfileDTO(
            methodology_id=self.methodology_id,
            version=self.version,
            health=health,
            confidence=final_confidence,
            reliability=reliability,
            applicability=applicability,
            provenance=provenance,
            evidence=EvidenceDTO(supporting_concepts=supporting, conflicting_concepts=conflicting, raw_evidence=[p.reason for p in provenance]),
            explainability=ExplainabilityDTO(
                why_applicable="Deviation and structural evidence" if is_applicable else "Insufficient capabilities",
                why_not_applicable="" if is_applicable else "Missing capabilities",
                supporting_evidence_summary=f"Severity: {severity_enum}, Structure: {structure_enum}",
                conflicting_evidence_summary="Trend risk" if regime == 1.0 else "None",
                required_conditions="Minimum Deviation Threshold",
                invalidating_conditions=", ".join(invalidating_conditions)
            ),
            execution_id=market_state.context.run_id,
            execution_timestamp=market_state.context.timestamp,
            scheduler_cadence="Every Candle",
            cache_status="MISS",
            validation_status="PENDING",
            state=state_enum,
            reference_value_type="Statistical", # In practice, this would be dynamically resolved based on what capabilities triggered it
            deviation_severity=severity_enum,
            expected_horizon="Short" if volatility_val > 0.5 else "Medium",
            reversion_target=reversion_target_enum,
            prob_initiation=prob_initiation,
            prob_completion=prob_completion,
            prob_failure=prob_failure,
            statistical_confidence=statistical_confidence,
            structural_confidence=structural_confidence,
            structure=structure_enum,
            regime_compatibility="Trending" if regime == 1.0 else "Transition" if regime == 0.5 else "Ranging",
            failure_conditions=failure_conditions
        )
        
        factors = ConfidenceFactorsDTO(factors={p.factor: p.contribution for p in provenance})
        
        # 5. Emit Raw Data metadata
        raw_data = {
            "is_applicable": is_applicable,
            "supporting_concepts": supporting,
            "conflicting_concepts": conflicting,
            "raw_evidence": [p.reason for p in provenance],
            "required_conditions": ["Minimum Deviation Threshold"],
            "invalidating_conditions": invalidating_conditions,
            
            # Embed structured metadata
            "Methodology Health": health,
            "Applicability Score": applicability,
            "Reliability Score": reliability,
            "MeanReversionProfile": profile,
            "Missing Dependencies": missing,
            "Scheduler Cadence": "Every Candle"
        }
        
        return factors, raw_data
