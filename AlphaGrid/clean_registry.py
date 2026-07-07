import yaml
import sys

def clean_registry():
    registry_path = 'master_capability_registry.yaml'
    
    with open(registry_path, 'r') as f:
        data = yaml.safe_load(f)
        
    capabilities = data.get('capabilities', [])
    
    required_by_someone = set()
    for cap in capabilities:
        reqs = cap.get('activation', {}).get('requires', [])
        opt_reqs = cap.get('activation', {}).get('optional_requires', [])
        required_by_someone.update(reqs)
        required_by_someone.update(opt_reqs)
        
    orphans = []
    for cap in capabilities:
        cid = cap.get('id')
        fam = cap.get('family', '')
        if cid not in required_by_someone and 'Strategy' not in fam:
            orphans.append(cid)
            
    print(f"Found {len(orphans)} orphans. Removing them...")
    
    cleaned_capabilities = [cap for cap in capabilities if cap.get('id') not in orphans]
    data['capabilities'] = cleaned_capabilities
    
    # Write back
    with open(registry_path, 'w') as f:
        yaml.dump(data, f, sort_keys=False, default_flow_style=False)
        
    print("Registry cleaned successfully.")

if __name__ == "__main__":
    clean_registry()
