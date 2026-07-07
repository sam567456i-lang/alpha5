import yaml

registry_path = r'C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\master_capability_registry.yaml'

with open(registry_path, 'r') as f:
    data = yaml.safe_load(f)

# Update cap_engine_composite_synthesis to use declarative pipeline instead of sequence list
for cap in data.get('capabilities', []):
    if cap.get('id') == 'cap_engine_composite_synthesis':
        # Remove old pipeline sequence
        if 'pipeline_sequence' in cap.get('metadata', {}):
            del cap['metadata']['pipeline_sequence']
        
        # Add detailed declarative pipeline
        cap['metadata']['pipeline'] = [
            {
                "stage": "Normalizer",
                "priority": 1,
                "dependencies": [],
                "failure_policy": "continue",
                "retry_policy": "none",
                "output_contract": "NormalizedMethodologyDict"
            },
            {
                "stage": "Compatibility",
                "priority": 2,
                "dependencies": ["Normalizer"],
                "failure_policy": "continue",
                "retry_policy": "none",
                "output_contract": "CompatibilityMatrix"
            },
            {
                "stage": "Interaction",
                "priority": 3,
                "dependencies": ["Normalizer", "Compatibility"],
                "failure_policy": "continue",
                "retry_policy": "none",
                "output_contract": "InteractionGraph"
            },
            {
                "stage": "Conflict",
                "priority": 4,
                "dependencies": ["Interaction"],
                "failure_policy": "continue",
                "retry_policy": "none",
                "output_contract": "ContradictionGraph"
            },
            {
                "stage": "Consensus",
                "priority": 5,
                "dependencies": ["Conflict"],
                "failure_policy": "continue",
                "retry_policy": "none",
                "output_contract": "ConsensusMetrics"
            },
            {
                "stage": "Evidence",
                "priority": 6,
                "dependencies": ["Consensus"],
                "failure_policy": "continue",
                "retry_policy": "none",
                "output_contract": "EvidenceDTO"
            },
            {
                "stage": "Explainability",
                "priority": 7,
                "dependencies": ["Evidence"],
                "failure_policy": "continue",
                "retry_policy": "none",
                "output_contract": "ExplainabilityDTO"
            },
            {
                "stage": "Intent",
                "priority": 8,
                "dependencies": ["Consensus"],
                "failure_policy": "fail_fast",
                "retry_policy": "none",
                "output_contract": "NumericalIntentVector"
            }
        ]

# Define Phase Exit governance gates directly in the registry
if 'governance' not in data:
    data['governance'] = {}

data['governance']['phase_exit_gates'] = [
    {"name": "Architecture Gate", "module": "ProjectOS.validator.architecture"},
    {"name": "Governance Gate", "module": "ProjectOS.validator.governance"},
    {"name": "Registry Gate", "module": "ProjectOS.validator.registry"},
    {"name": "Documentation Gate", "module": "ProjectOS.validator.documentation"},
    {"name": "Testing Gate", "module": "ProjectOS.validator.testing"},
    {"name": "Certification Gate", "module": "ProjectOS.validator.certification"},
    {"name": "Replay Gate", "module": "ProjectOS.validator.replay"},
    {"name": "Performance Gate", "module": "ProjectOS.validator.performance"}
]

with open(registry_path, 'w') as f:
    yaml.dump(data, f, sort_keys=False, default_flow_style=False)

print("Registry updated with declarative synthesis pipeline and phase exit gates.")
