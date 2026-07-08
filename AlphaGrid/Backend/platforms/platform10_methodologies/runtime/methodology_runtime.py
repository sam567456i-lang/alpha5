from Backend.core.interfaces.methodology_context_dto import MethodologyContextDTO
from Backend.platforms.platform10_methodologies.engines.methodology_state_machine import MethodologyStateMachine
from Backend.platforms.platform10_methodologies.engines.methodology_policy_engine import MethodologyPolicyEngine
from Backend.platforms.platform10_methodologies.engines.methodology_conflict_engine import MethodologyConflictEngine
from Backend.platforms.platform10_methodologies.engines.methodology_consensus_engine import MethodologyConsensusEngine
from Backend.core.resolvers.registry_resolver import RegistryResolver

class MethodologyRuntime:
    """
    The orchestrator for Platform 10.
    Manages the lifecycle of methodology evaluation, delegating to explicit engines.
    """
    def __init__(self, registry_dir: str):
        self.resolver = RegistryResolver(registry_dir)
        self.conflict_engine = MethodologyConflictEngine()
        self.consensus_engine = MethodologyConsensusEngine()

    def evaluate_context(self, context: MethodologyContextDTO, active_plugins: list):
        # 1. Resolve State Machine config
        sm_config = self.resolver.resolve_state_machine_config()
        state_machine = MethodologyStateMachine(sm_config)
        
        # 2. Pre-flight rejection
        valid_plugins = []
        for plugin in active_plugins:
            caps = plugin.get_capabilities()
            if context.market_identity not in caps.get("markets", []):
                # Reject unsupported market
                continue
            if context.execution_mode.mode.name not in caps.get("execution_modes", []):
                # Reject unsupported mode
                continue
            valid_plugins.append(plugin)
            
        # 3. Evaluate only valid plugins
        mock_assessments = []
        for p in valid_plugins:
            mock_assessments.append(p.evaluate(context))
        
        # 4. Detect Conflicts
        conflicts = self.conflict_engine.detect_conflicts(mock_assessments)
        
        # 5. Generate Consensus
        consensus = self.consensus_engine.generate_consensus(mock_assessments, conflicts)
        
        # 6. Builder/Factory (mocked return for now)
        return {
            "assessments": mock_assessments,
            "consensus": consensus
        }
