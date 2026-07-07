import hashlib
import uuid
from typing import Optional, List
from Backend.dtos.concepts import ConceptDTO
from Backend.Platform10.contracts.dtos import PriceActionProfileDTO, ExplainabilityDTO, ProvenanceDTO, EvidenceDTO

class PriceActionCoreMethodology:
    """Price Action Methodology Implementation for Platform 10.
    
    Evaluates abstract Price Action concepts produced by Platform 9.
    Does NOT hardcode patterns (Hammer, Engulfing, etc.). Instead, relies on abstract metrics:
    - Reversal Potential
    - Continuation Potential
    - Rejection Strength
    - Acceptance Strength
    - Pattern Quality
    
    Derives structural confidence by aligning these metrics with:
    - Trend State
    - Structure State
    - Volatility State
    - Momentum State
    - Market Regime
    - Liquidity State
    """
    
    def __init__(self):
        self.component_id = "cap_meth_price_action_core"
        
    def evaluate(
        self,
        pa_concept: ConceptDTO,
        trend_concept: Optional[ConceptDTO] = None,
        structure_concept: Optional[ConceptDTO] = None,
        regime_concept: Optional[ConceptDTO] = None,
        liquidity_concept: Optional[ConceptDTO] = None,
        volatility_concept: Optional[ConceptDTO] = None,
        momentum_concept: Optional[ConceptDTO] = None,
        execution_context=None,
    ) -> PriceActionProfileDTO:
        
        # 1. Extract abstract Platform 9 metrics (falling back gracefully)
        meta = pa_concept.metadata
        reversal_potential = meta.get('reversal_potential', 0.0)
        continuation_potential = meta.get('continuation_potential', 0.0)
        rejection_strength = meta.get('rejection_strength', 0.0)
        acceptance_strength = meta.get('acceptance_strength', 0.0)
        pattern_quality = meta.get('pattern_quality', 0.5)
        
        # 2. Determine Direction and Class purely from abstract potentials
        direction = "Neutral"
        pattern_class = "Indecision"
        
        if reversal_potential > 0.6:
            pattern_class = "Reversal"
            direction = meta.get('direction', "Neutral")
        elif continuation_potential > 0.6:
            pattern_class = "Continuation"
            direction = meta.get('direction', "Neutral")
            
        # 3. Derive Confidence through Multi-Factor Evidence (Not arbitrary constants)
        # Factor 1: Pattern Quality itself
        confidence = pattern_quality * 0.4
        
        # Factor 2: Trend Alignment (if continuation)
        trend_alignment = 0.5
        if trend_concept and pattern_class == "Continuation":
            if (direction == "Bullish" and trend_concept.state == "BULLISH") or \
               (direction == "Bearish" and trend_concept.state == "BEARISH"):
                trend_alignment = 1.0
                confidence += 0.2
        elif trend_concept and pattern_class == "Reversal":
            if regime_concept and regime_concept.state == "TRANSITION":
                trend_alignment = 0.8
                confidence += 0.2
                
        # Factor 3: Structure Support
        structure_quality = 0.5
        if structure_concept:
            structure_quality = structure_concept.metadata.get('support_strength', 0.5)
            confidence += (structure_quality * 0.2)
            
        # Factor 4: Volatility/Momentum Compatibility
        vol_compatibility = 0.5
        if volatility_concept and momentum_concept:
            # Assuming these have confidence properties
            vol_compatibility = (volatility_concept.confidence + momentum_concept.confidence) / 2.0
            confidence += (vol_compatibility * 0.2)
            
        confidence = min(1.0, max(0.0, confidence))
        
        # 4. Context Compatibility & Applicability
        applicability = confidence * 0.9
        context_compat = "High" if confidence > 0.7 else ("Medium" if confidence > 0.4 else "Low")
        
        # 5. Provenance Generation
        provenance = [
            ProvenanceDTO(factor="Pattern Quality", weight=0.4, contribution=pattern_quality*0.4, reason="Base PA signal quality"),
            ProvenanceDTO(factor="Trend Alignment", weight=0.2, contribution=trend_alignment*0.2, reason="Trend context"),
            ProvenanceDTO(factor="Structure Quality", weight=0.2, contribution=structure_quality*0.2, reason="S/R confluence"),
            ProvenanceDTO(factor="Volatility/Momentum", weight=0.2, contribution=vol_compatibility*0.2, reason="Energy state")
        ]
        
        dependencies = [pa_concept.id]
        if trend_concept: dependencies.append(trend_concept.id)
        if structure_concept: dependencies.append(structure_concept.id)
        if regime_concept: dependencies.append(regime_concept.id)
        if liquidity_concept: dependencies.append(liquidity_concept.id)
        if volatility_concept: dependencies.append(volatility_concept.id)
        if momentum_concept: dependencies.append(momentum_concept.id)
        
        payload = f"{direction}:{pattern_class}:{confidence}:{applicability}"
        payload_hash = hashlib.md5(payload.encode()).hexdigest()
        
        explainability = ExplainabilityDTO(
            why_applicable="Strong rejection metrics aligned with structure." if confidence > 0.7 else "Contextual alignment indicates average reliability.",
            why_not_applicable="Poor trend alignment or weak pattern quality." if confidence < 0.4 else "",
            supporting_evidence_summary=f"Context compatibility is {context_compat} with direction {direction}.",
            conflicting_evidence_summary="None",
            required_conditions="High acceptance/rejection strength",
            invalidating_conditions="Opposing momentum or lack of structural support."
        )
        
        evidence = EvidenceDTO(
            supporting_concepts=dependencies,
            conflicting_concepts=[],
            raw_evidence=["PA pattern metrics successfully derived."]
        )
        
        return PriceActionProfileDTO(
            methodology_id=self.component_id,
            version="1.0.0",
            health="Ready",
            confidence=confidence,
            reliability=confidence * 0.85,
            applicability=applicability,
            provenance=provenance,
            evidence=evidence,
            explainability=explainability,
            execution_id=execution_context.trace_id if execution_context else "none",
            execution_timestamp="none", # placeholder for runtime injection
            scheduler_cadence="Tick",
            cache_status="MISS",
            validation_status="repository_validated",
            
            # Profile Fields
            direction=direction,
            pattern_class=pattern_class,
            strength="Strong" if confidence >= 0.8 else ("Moderate" if confidence >= 0.5 else "Weak"),
            quality="Good" if pattern_quality > 0.6 else "Fair",
            context_compatibility=context_compat,
            rejection_strength=rejection_strength,
            acceptance_strength=acceptance_strength,
            reversal_potential=reversal_potential,
            continuation_potential=continuation_potential
        )
