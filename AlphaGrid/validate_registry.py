import yaml
import sys

def validate_registry():
    registry_path = r'C:\Users\praka\.gemini\antigravity\brain\e5c38fbb-20c7-49d7-bb09-1233d320f032\master_capability_registry.yaml'
    
    try:
        with open(registry_path, 'r') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"ERROR: Could not find registry at {registry_path}")
        sys.exit(1)
        
    capabilities = data.get('capabilities', [])
    
    print("=========================================")
    print("CAPABILITY REGISTRY HEALTH AUDIT")
    print("=========================================")
    
    ids = set()
    duplicates = []
    for cap in capabilities:
        cid = cap.get('id')
        if cid in ids:
            duplicates.append(cid)
        ids.add(cid)
        
    print(f"\n1. Duplicate Registrations: {len(duplicates)}")
    if duplicates:
        print(f"   Details: {duplicates}")
        
    # Check orphans (capabilities nobody requires, except strategies)
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
            # Note: External APIs, Market Data, etc might be orphans in a partial build
            orphans.append(cid)
            
    # For this strict audit, we just list them. True orphans are bad, but entrypoints are expected.
    print(f"\n2. Non-Strategy Orphan Capabilities: {len(orphans)}")
    if orphans:
        print(f"   Details: {orphans}")
        
    # Circular dependencies
    # Build graph
    graph = {}
    for cap in capabilities:
        cid = cap.get('id')
        reqs = cap.get('activation', {}).get('requires', [])
        graph[cid] = reqs
        
    def check_cycle(node, visited, path):
        visited.add(node)
        path.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if check_cycle(neighbor, visited, path):
                    return True
            elif neighbor in path:
                return True
                
        path.pop()
        return False
        
    has_cycle = False
    for node in graph:
        if check_cycle(node, set(), []):
            has_cycle = True
            break
            
    print(f"\n3. Circular Dependencies Found: {has_cycle}")
    
    print(f"\nTotal Capabilities Validated: {len(capabilities)}")

if __name__ == "__main__":
    validate_registry()
