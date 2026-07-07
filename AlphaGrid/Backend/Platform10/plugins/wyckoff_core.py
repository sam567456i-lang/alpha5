from Backend.Platform10.contracts.dtos import (
    MarketStateDTO, MethodologyResultDTO, WyckoffProfileDTO,
    EvidenceDTO, ExplainabilityDTO, ExecutionContext
)
from Backend.Platform9.contracts.dtos import (
    AccumulationConcept, DistributionConcept
)

class WyckoffCore:
    __version__ = "v1.0"
    __dto_version__ = "v1.0"
    __schema_version__ = "v1.0"
    
    def execute(self, state: MarketStateDTO) -> MethodologyResultDTO:
        concepts = state.concepts.concepts
        
        has_acc = any(isinstance(c, AccumulationConcept) for c in concepts.values())
        has_dist = any(isinstance(c, DistributionConcept) for c in concepts.values())
        
        score = 0.8 if has_acc else (0.2 if has_dist else 0.5)
        bias = "Accumulation" if has_acc else "Distribution"
        
        profile = WyckoffProfileDTO(
            methodology_id="p10_wyckoff",
            version=self.__version__,
            health="HEALTHY",
            confidence=score,
            reliability=0.8,
            applicability=1.0,
            provenance=[],
            evidence=EvidenceDTO(supporting_concepts=[], conflicting_concepts=[], raw_evidence=[]),
            explainability=ExplainabilityDTO("", "", "", "", "", ""),
            execution_id=state.context.run_id,
            execution_timestamp=state.context.timestamp,
            scheduler_cadence="BAR",
            cache_status="MISS",
            validation_status="VALID",
            phase="Phase C",
            composite_operator_bias=bias,
            spring_or_upthrust=True,
            sos_or_sow=True,
            markup_markdown_potential="High"
        )
        
        return MethodologyResultDTO(
            methodology_id="p10_wyckoff",
            version=self.__version__,
            plugin_id="WyckoffCore",
            execution_id=state.context.run_id,
            execution_context=state.context,
            score=score,
            confidence=score,
            strength=score,
            evidence=profile.evidence,
            supporting_concepts=[],
            conflicting_concepts=[],
            preconditions=[],
            failure_reasons=[],
            explainability=profile.explainability,
            metadata={"profile": profile},
            execution_duration_ms=25.0,
            validation_status="VALID"
        )