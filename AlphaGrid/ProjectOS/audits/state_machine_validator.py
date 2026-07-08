import os
import yaml
from collections import Counter

def validate_state_machine_registry(registry_path: str):
    print(f"Validating State Machine Registry at {registry_path}...")
    if not os.path.exists(registry_path):
        print("FAIL: Registry not found.")
        return False

    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = yaml.safe_load(f)

    # 1. Versioning
    version_info = registry.get("version")
    if not version_info or "schema" not in version_info:
        print("FAIL: Missing schema version.")
        return False
        
    states = registry.get("states", {})
    terminal_states = registry.get("terminal_states", {})
    recovery_states = registry.get("recovery_states", {})
    event_priority = registry.get("event_priority", {})
    illegal_transitions = registry.get("illegal_transitions", [])
    
    all_declared_states = set(states.keys()).union(set(terminal_states.keys())).union(set(recovery_states.keys()))

    # 2. Duplicate Priorities
    priority_values = list(event_priority.values())
    priority_counts = Counter(priority_values)
    duplicates = [p for p, count in priority_counts.items() if count > 1]
    if duplicates:
        print(f"FAIL: Duplicate event priorities found for values {duplicates}. Priorities must be strictly unique to guarantee deterministic tie-breaking.")
        return False

    # 3. Unreachable/Orphan States & Dead Ends
    reachable_states = {"BULLISH", "BEARISH", "CONSOLIDATION", "UNKNOWN", "PULLBACK"} # Entry points
    used_events = set()
    
    for state_name, events in states.items():
        for event_id, transition in events.items():
            used_events.add(event_id)
            next_state = transition.get("next")
            if next_state:
                reachable_states.add(next_state)
                if next_state not in all_declared_states:
                    print(f"FAIL: Transition from {state_name} via {event_id} points to undefined state: {next_state}")
                    return False
                
                # 4. Impossible Transitions (against illegal_transitions)
                transition_str = f"{state_name} -> {next_state}"
                if transition_str in illegal_transitions:
                    print(f"FAIL: State machine defines a transition ({transition_str}) that is explicitly marked as illegal.")
                    return False

    unreachable = all_declared_states - reachable_states
    if unreachable:
        print(f"WARNING: Unreachable states found: {unreachable}")

    # 5. Unused Events
    declared_events = set(event_priority.keys())
    unused = declared_events - used_events
    if unused:
        print(f"WARNING: Events {unused} have priorities assigned but are not used in any transition guards.")

    print("PASS: State Machine Registry validation successful.")
    return True

if __name__ == "__main__":
    registry_path = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Docs\Governance\registry\state_machine_registry.yaml"
    success = validate_state_machine_registry(registry_path)
    if not success:
        exit(1)
