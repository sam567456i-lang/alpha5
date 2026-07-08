import yaml
from typing import Dict, List, Optional, Any
from Backend.shared_domain.contracts.structure.structure_dtos import (
    StructureStateDTO,
    StructureEventDTO,
    StructureContextDTO
)

class InvalidStructureTransitionError(Exception):
    pass

class OutOfOrderEventError(Exception):
    pass

class AlreadyProcessedEventError(Exception):
    pass

class RegistryVersionMismatchError(Exception):
    pass

class StructureStateMachine:
    """
    Immutable, stateless Finite State Machine governing valid Market Structure transitions.
    Fully data-driven via Docs/Governance/registry/state_machine_registry.yaml.
    """
    
    def __init__(self, registry_path: str = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Docs\Governance\registry\state_machine_registry.yaml"):
        self.registry_path = registry_path
        self._load_registry()

    def _load_registry(self):
        import hashlib
        import json
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            self._registry_str = f.read()
            self._registry = yaml.safe_load(self._registry_str)
            
        self._registry_checksum = hashlib.sha256(self._registry_str.encode('utf-8')).hexdigest()
        self.states = self._registry.get('states', {})
        self.event_priority = self._registry.get('event_priority', {})
        self.illegal_transitions = self._registry.get('illegal_transitions', [])
        
        self.version_info = self._registry.get("version", {})
        self.schema_version = self.version_info.get("schema", "1.0.0")

    def process_event(self, current_context: StructureContextDTO, event: StructureEventDTO) -> StructureContextDTO:
        """
        Purely stateless transition function.
        Receives current state and event, returns entirely new state context.
        """
        # 0. Version / Checksum Check for deterministic replay
        if current_context.registry_checksum and current_context.registry_checksum != self._registry_checksum:
             raise RegistryVersionMismatchError(f"Context checksum {current_context.registry_checksum} does not match engine {self._registry_checksum}")
             
        # 1. Replay Identity / Idempotency Check
        if event.id == getattr(current_context, 'last_event_id', None) and event.timestamp == current_context.last_updated_timestamp:
            raise AlreadyProcessedEventError(f"Event {event.id} already processed.")

        # 2. Out-of-Order Check (Sequence Number -> Timestamp)
        if event.sequence_number < current_context.sequence_number:
            raise OutOfOrderEventError(f"Sequence {event.sequence_number} arrived after {current_context.sequence_number}")
        elif event.sequence_number == current_context.sequence_number:
            if event.timestamp < current_context.last_updated_timestamp:
                raise OutOfOrderEventError(f"Timestamp {event.timestamp} arrived after {current_context.last_updated_timestamp}")
                
            # 3. Event Priority Handling (same sequence and timestamp)
            elif event.timestamp == current_context.last_updated_timestamp:
                last_event_id = getattr(current_context, 'last_event_id', None)
                if last_event_id:
                    current_priority = self.event_priority.get(last_event_id, 0)
                    new_priority = self.event_priority.get(event.id, 0)
                    if new_priority <= current_priority:
                        # New event loses priority tie-breaker, ignore
                        return current_context

        # 4. State Transition Resolution
        current_state_str = current_context.current_state.name
        event_key = event.id # e.g., "str.eve.bos.major"
        
        state_def = self.states.get(current_state_str, {})
        transition = state_def.get(event_key)
        
        if not transition:
            # Event does not trigger a state transition for the current state.
            next_state_str = current_state_str
        else:
            # 5. Guard Evaluation (simplistic mock for now)
            guards = transition.get('guards', {})
            guards_passed = True
            for guard_key, guard_val in guards.items():
                # In a real FSM, we'd have a guard evaluator
                if guard_key == "minimum_strength" and getattr(event, "strength", 1.0) < guard_val:
                    guards_passed = False
                    
            if guards_passed:
                next_state_str = transition.get('next', current_state_str)
            else:
                next_state_str = current_state_str
                
        # 6. Validate Illegal Transitions
        transition_str = f"{current_state_str} -> {next_state_str}"
        if transition_str in self.illegal_transitions:
            raise InvalidStructureTransitionError(f"Transition {transition_str} is explicitly illegal in registry.")
            
        next_state = getattr(StructureStateDTO, next_state_str, StructureStateDTO.UNKNOWN)

        # 7. Return new Context
        new_context = StructureContextDTO(
            id=f"{current_context.identity.symbol}_{current_context.identity.timeframe}_context",
            timestamp=event.timestamp,
            consumes=[],
            produces=[],
            identity=current_context.identity,
            current_state=next_state,
            sequence_number=event.sequence_number,
            last_updated_timestamp=event.timestamp,
            registry_checksum=self._registry_checksum,
            state_machine_version=self.schema_version
        )
        object.__setattr__(new_context, 'last_event_id', event.id)
        return new_context
