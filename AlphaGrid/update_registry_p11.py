import yaml

registry_path = r'C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\master_capability_registry.yaml'

with open(registry_path, 'r') as f:
    data = yaml.safe_load(f)

# The user explicitly asked for abstract semantic interaction policies instead of numeric multipliers
# For Platform 11, we will register the overarching Composite Methodology Engine.
platform_11_capabilities = [
    {
        'id': 'cap_engine_composite_synthesis',
        'category': 'Synthesis',
        'family': 'Institutional Synthesis',
        'name': 'Composite Methodology Synthesis Engine',
        'platform': 'Platform 11',
        'version': '1.0.0',
        'implementation_status': 'implemented',
        'lifecycle_state': 'Frozen', # It's what we are building
        'activation': {
            'enabled': True,
            'required_phase': 11
        },
        'metadata': {
            'interaction_policies': [
                'Increase Weight',
                'Reduce Uncertainty',
                'Increase Reliability',
                'Add Supporting Evidence',
                'Suppress',
                'Reduce Applicability',
                'Increase Conflict'
            ],
            'pipeline_sequence': [
                'Normalizer',
                'Compatibility',
                'Interaction',
                'Conflict',
                'Consensus',
                'Evidence',
                'Explainability',
                'Intent'
            ]
        }
    }
]

# Ensure no duplicates
existing_ids = {cap['id'] for cap in data.get('capabilities', [])}
for new_cap in platform_11_capabilities:
    if new_cap['id'] not in existing_ids:
        data['capabilities'].append(new_cap)

with open(registry_path, 'w') as f:
    yaml.dump(data, f, sort_keys=False, default_flow_style=False)

print("Appended Platform 11 capabilities to registry.")
