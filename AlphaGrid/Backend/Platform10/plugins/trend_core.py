from typing import Dict, Any, Tuple
from Backend.Platform10.contracts.interfaces import IMethodologyPlugin
from Backend.Platform10.contracts.dtos import MarketStateDTO, ConfidenceFactorsDTO, TrendProfileDTO, ProvenanceDTO, EvidenceDTO, ExplainabilityDTO

class TrendCoreMethodology(IMethodologyPlugin):
    """Wave 1: Institutional Core Trend Methodology (Capability-Driven)"""
    
    @property
    def methodology_id(self) -> str:
        return "cap_meth_trend_core"
        
    @property
    def version(self) -> str:
        return "1.0.0"
        
    @property
    def capability_family(self) -> str:
        return "trend"

    def evaluate_factors(self, market_state: MarketStateDTO) -> Tuple[ConfidenceFactorsDTO, Dict[str, Any]]:
        features = market_state.features.features
        
        # 1. Methodology Health (Graceful degradation)
        health = "Ready"
        required = ["TrendStructure", "TrendDirection", "TrendPersistence", "MarketRegime", "Momentum", "Volatility", "PricePosition"]
        missing = [f for f in required if f not in features]
        if missing:
            health = "Partial" if len(missing) < 3 else "Degraded"
            
        # Abstract Capability Consumption
        # Note: In a real environment, the plugin would parse the abstract scalar/vector values from these features
        # We will mock the resolution logic using simple synthetic values derived from the abstracted inputs.
        struct_val = features.get("TrendStructure", 0.0)
        direction_val = features.get("TrendDirection", 1.0)
        regime = features.get("MarketRegime", 1.0) # 1=Trend, 0=Consolidation
        momentum = features.get("Momentum", 0.5)
        
        is_applicable = True
        direction_enum = "Bullish" if direction_val > 0 else "Bearish" if direction_val < 0 else "Neutral"
        
        # 2. Invalidation Conditions
        invalidating_conditions = []
        if regime == -1.0: # Macro Reversal
            invalidating_conditions.append("Macro regime reversal")
        if momentum < 0.1:
            invalidating_conditions.append("Momentum collapse")
            
        # 3. Market Regime Compatibility
        compatibility = 1.0 if regime == 1.0 else 0.6 if regime > 0 else 0.2
        
        # 4. Confidence Provenance
        provenance = [
            ProvenanceDTO("Trend Strength", 0.4, 0.4 * momentum, "Sustained directional momentum"),
            ProvenanceDTO("Market Regime", 0.3, 0.3 * compatibility, "Regime compatibility alignment"),
            ProvenanceDTO("Structure", 0.3, 0.3 * struct_val, "Structural continuation"),
        ]
        
        final_confidence = sum(p.contribution for p in provenance)
        
        profile = TrendProfileDTO(
            methodology_id=self.methodology_id,
            version=self.version,
            health=health,
            confidence=final_confidence,
            reliability=1.0,
            applicability=1.0, # Simple for trend
            provenance=provenance,
            evidence=EvidenceDTO(supporting_concepts=["Directional Alignment"] if direction_enum != "Neutral" else [], conflicting_concepts=["Regime Mismatch"] if regime < 1.0 else [], raw_evidence=[p.reason for p in provenance]),
            explainability=ExplainabilityDTO(
                why_applicable="Trend features detected",
                why_not_applicable="",
                supporting_evidence_summary="Strong trend",
                conflicting_evidence_summary="None",
                required_conditions="Structural Alignment",
                invalidating_conditions=", ".join(invalidating_conditions)
            ),
            execution_id=market_state.context.run_id,
            execution_timestamp=market_state.context.timestamp,
            scheduler_cadence="Every Candle",
            cache_status="MISS",
            validation_status="PENDING",
            direction=direction_enum,
            strength="Strong" if momentum > 0.7 else "Moderate" if momentum > 0.4 else "Weak",
            quality="Good" if struct_val > 0.5 else "Poor",
            persistence="High" if features.get("TrendPersistence", 0.0) > 0.7 else "Low",
            maturity="Established",
            regime="Trending" if regime == 1.0 else "Consolidating"
        )
        
        factors = ConfidenceFactorsDTO(factors={p.factor: p.contribution for p in provenance})
        
        # We pass the rich structs back via raw_data to be embedded in metadata by the engine
        raw_data = {
            "is_applicable": is_applicable,
            "supporting_concepts": ["Directional Alignment"] if direction_enum != "Neutral" else [],
            "conflicting_concepts": ["Regime Mismatch"] if regime < 1.0 else [],
            "raw_evidence": [p.reason for p in provenance],
            "required_conditions": ["Structural Alignment"],
            "invalidating_conditions": invalidating_conditions,
            
            # Embed structured metadata
            "Methodology Health": health,
            "TrendProfile": profile,
            "Confidence Provenance": provenance,
            "Missing Dependencies": missing
        }
        
        return factors, raw_data
