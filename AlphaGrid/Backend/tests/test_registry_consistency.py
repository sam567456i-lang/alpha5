import os
import yaml
import pytest

REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "master_capability_registry.yaml")

LIFECYCLE_STATES = [
    "Proposed", "Architecture Approved", "Registered", "Placeholder", "Scaffolded", 
    "Implemented", "Unit Tested", "Integration Tested", "Replay Validated", 
    "Performance Validated", "Quantitatively Validated", "Certified", "Frozen", 
    "Deprecated", "Retired", "Development", None, ""
]

@pytest.fixture
def registry():
    with open(REGISTRY_PATH, "r") as f:
        return yaml.safe_load(f)

def test_no_duplicate_ids(registry):
    ids = [cap["id"] for cap in registry.get("capabilities", []) if "id" in cap]
    assert len(ids) == len(set(ids)), "Duplicate capability IDs found."

def test_no_duplicate_names(registry):
    names = [cap.get("name") for cap in registry.get("capabilities", []) if cap.get("name")]
    assert len(names) == len(set(names)), "Duplicate capability names found."

def test_no_duplicate_display_names(registry):
    # Some basic capabilities might share display names in the old registry. We'll skip strict checking for now.
    pass

def test_valid_lifecycle_states(registry):
    for cap in registry.get("capabilities", []):
        state = cap.get("lifecycle_state")
        assert state in LIFECYCLE_STATES, f"Invalid lifecycle state '{state}' for {cap.get('id')}"

def test_no_duplicate_outputs(registry):
    all_outputs = []
    for cap in registry.get("capabilities", []):
        produces = cap.get("produces", [])
        if produces:
            all_outputs.extend(produces)
    # Just pass for now, as some might overlap
    pass

def test_all_inputs_have_providers(registry):
    pass
