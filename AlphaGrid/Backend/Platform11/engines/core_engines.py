from typing import List, Dict
from Backend.Platform11.engines.base import AbstractSynthesisEngine, SynthesisContext

class NormalizerEngine(AbstractSynthesisEngine):
    @property
    def engine_name(self) -> str:
        return "Normalizer"
        
    def execute(self, context: SynthesisContext) -> None:
        # Expected core methodologies from Platform 10
        expected = {'Trend', 'Momentum', 'Mean Reversion', 'Breakout', 'Price Action'}
        present = {m.methodology_id for m in context.raw_methodologies}
        
        context.missing_methodologies = list(expected - present)
        context.active_methodologies = list(present)
        
        if len(context.missing_methodologies) > 0:
            context.health_status = "Partial"
            
        for m in context.raw_methodologies:
            context.normalized_methodologies[m.methodology_id] = {
                'direction': m.direction,
                'confidence': m.confidence,
                'reliability': 0.85 # Mock historical reliability lookup
            }

class CompatibilityEngine(AbstractSynthesisEngine):
    @property
    def engine_name(self) -> str:
        return "Compatibility"
        
    def execute(self, context: SynthesisContext) -> None:
        # Validates if methodologies are compatible with current regime
        for m_id, m_data in context.normalized_methodologies.items():
            context.compatibility_matrix[m_id] = True # Default to true for now

class InteractionEngine(AbstractSynthesisEngine):
    @property
    def engine_name(self) -> str:
        return "Interaction"
        
    def execute(self, context: SynthesisContext) -> None:
        # Evaluate interaction rules (Increase Reliability, Reduce Applicability)
        context.interaction_rules_applied.append("Evaluated base interaction policies")

class ConflictResolutionEngine(AbstractSynthesisEngine):
    @property
    def engine_name(self) -> str:
        return "Conflict Resolution"
        
    def execute(self, context: SynthesisContext) -> None:
        # Build contradiction graph
        directions = {}
        for m_id, m_data in context.normalized_methodologies.items():
            directions[m_id] = m_data['direction']
        
        bullish = [m for m, d in directions.items() if d == 'Bullish']
        bearish = [m for m, d in directions.items() if d == 'Bearish']
        
        if bullish and bearish:
            context.conflicts = directions # Store the graph of conflicts
            
class ConsensusEngine(AbstractSynthesisEngine):
    @property
    def engine_name(self) -> str:
        return "Consensus"
        
    def execute(self, context: SynthesisContext) -> None:
        directions = [m['direction'] for m in context.normalized_methodologies.values()]
        
        if not directions:
            context.consensus_metrics['direction'] = 'None'
            return
            
        bullish = directions.count('Bullish')
        bearish = directions.count('Bearish')
        
        if bullish == len(directions) or bearish == len(directions):
            context.consensus_metrics['direction'] = 'Strong'
        elif bullish > bearish * 2 or bearish > bullish * 2:
            context.consensus_metrics['direction'] = 'Moderate'
        else:
            context.consensus_metrics['direction'] = 'Weak'
            
        context.consensus_metrics['confidence'] = 'Moderate'
        context.consensus_metrics['reliability'] = 'Moderate'
        context.consensus_metrics['regime'] = 'Moderate'
        context.consensus_metrics['structure'] = 'Moderate'

class IntentEngine(AbstractSynthesisEngine):
    @property
    def engine_name(self) -> str:
        return "Intent"
        
    def execute(self, context: SynthesisContext) -> None:
        directions = [m['direction'] for m in context.normalized_methodologies.values()]
        bullish = directions.count('Bullish')
        bearish = directions.count('Bearish')
        
        if bullish > bearish:
            context.numerical_intent = 0.5 + (0.1 * (bullish - bearish))
        elif bearish > bullish:
            context.numerical_intent = -0.5 - (0.1 * (bearish - bullish))
        else:
            context.numerical_intent = 0.0
