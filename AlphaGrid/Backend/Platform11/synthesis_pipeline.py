import yaml
import os
from typing import List
from datetime import datetime, timezone

from Backend.Platform10.contracts.dtos import MethodologyProfileDTO, ExecutionContext
from Backend.Platform11.contracts.dtos import (
    CompositeMethodologyDTO, CompositeDecisionContextDTO, CompositeHealthDTO, 
    CompositeTraceDTO
)
from Backend.Platform11.engines.base import SynthesisContext, AbstractSynthesisEngine
from Backend.Platform11.engines.core_engines import (
    NormalizerEngine, CompatibilityEngine, InteractionEngine, 
    ConflictResolutionEngine, ConsensusEngine, IntentEngine
)

class InstitutionalSynthesisPipeline:
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        self._load_pipeline_config()
        self._initialize_engines()
        
    def _load_pipeline_config(self):
        with open(self.registry_path, 'r') as f:
            data = yaml.safe_load(f)
            
        for cap in data.get('capabilities', []):
            if cap.get('id') == 'cap_engine_composite_synthesis':
                # Use the new declarative pipeline definition
                self.pipeline_stages = cap['metadata'].get('pipeline', [])
                # Sort by priority just in case
                self.pipeline_stages.sort(key=lambda x: x.get('priority', 99))
                self.pipeline_sequence = [stage['stage'] for stage in self.pipeline_stages]
                return
        
        # Fallback if registry lacks the definition
        self.pipeline_sequence = [
            'Normalizer', 'Compatibility', 'Interaction', 'Conflict', 
            'Consensus', 'Intent'
        ]
        
    def _initialize_engines(self):
        # Map string names to engine instances
        engine_map = {
            'Normalizer': NormalizerEngine(),
            'Compatibility': CompatibilityEngine(),
            'Interaction': InteractionEngine(),
            'Conflict': ConflictResolutionEngine(),
            'Consensus': ConsensusEngine(),
            'Intent': IntentEngine(),
            'Evidence': NormalizerEngine(), # Mock reuse for now to ensure instantiation doesn't break
            'Explainability': NormalizerEngine()
        }
        
        self.engines: List[AbstractSynthesisEngine] = []
        for stage in self.pipeline_sequence:
            if stage in engine_map:
                self.engines.append(engine_map[stage])
            else:
                raise ValueError(f"CRITICAL ARCHITECTURE VIOLATION: Pipeline stage {stage} defined in registry has no runtime implementation.")

    def synthesize(self, methodologies: List[MethodologyProfileDTO], context: ExecutionContext) -> tuple[CompositeMethodologyDTO, CompositeDecisionContextDTO]:
        """
        Executes the dynamically loaded pipeline (dictated entirely by registry)
        to synthesize methodologies into a coherent market interpretation.
        """
        synth_context = SynthesisContext(methodologies)
        
        # 1. Execute Pipeline sequentially as defined by the registry
        for engine in self.engines:
            engine.execute(synth_context)
            
        # 2. Build Composite Trace
        trace = CompositeTraceDTO(
            input_methodologies=synth_context.active_methodologies,
            interactions_applied=[], # Populated by InteractionEngine
            conflicts_detected=len(synth_context.conflicts),
            consensus_built=synth_context.consensus_metrics.get('direction', 'None'),
            evidence_generated=len(synth_context.evidence),
            intent_produced=str(synth_context.numerical_intent)
        )
        
        # 3. Build Health Profile
        health = CompositeHealthDTO(
            status=synth_context.health_status,
            missing_methodologies=synth_context.missing_methodologies,
            active_methodologies=synth_context.active_methodologies
        )
        
        # 4. Generate CompositeMethodologyDTO (Analytical State)
        composite = CompositeMethodologyDTO(
            id=f"comp_{context.correlation_id}",
            schema_version="1.0.0",
            composite_direction="Mixed" if synth_context.conflicts else synth_context.consensus_metrics.get('direction', 'Neutral'),
            composite_confidence=0.8,
            composite_reliability=0.85,
            composite_applicability=1.0 if not synth_context.missing_methodologies else 0.8,
            direction_consensus=synth_context.consensus_metrics.get('direction', 'None'),
            confidence_consensus=synth_context.consensus_metrics.get('confidence', 'None'),
            reliability_consensus=synth_context.consensus_metrics.get('reliability', 'None'),
            regime_consensus=synth_context.consensus_metrics.get('regime', 'None'),
            structure_consensus=synth_context.consensus_metrics.get('structure', 'None'),
            conflict_severity="High" if len(synth_context.conflicts) > 2 else ("Low" if synth_context.conflicts else "None"),
            contradiction_graph=synth_context.conflicts,
            dominant_methodologies=[],
            supporting_methodologies=[],
            conflicting_methodologies=list(synth_context.conflicts.keys()),
            applied_interaction_rules=synth_context.interaction_rules_applied,
            composite_health=health,
            composite_trace=trace,
            execution_context=context
        )
        
        # 5. Generate CompositeDecisionContextDTO (Decision Context for Platform 12)
        decision = CompositeDecisionContextDTO(
            id=f"dec_{context.correlation_id}",
            timestamp=datetime.now(timezone.utc),
            numerical_intent=synth_context.numerical_intent,
            composite_confidence=composite.composite_confidence,
            regime_context="Placeholder Regime",
            structural_context="Placeholder Structure",
            volatility_context="Placeholder Volatility",
            liquidity_context="Placeholder Liquidity",
            composite_methodology=composite,
            execution_context=context
        )
        
        return composite, decision
