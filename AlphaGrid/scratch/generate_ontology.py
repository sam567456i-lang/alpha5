import os
import yaml

def generate_ontology(repo_root: str):
    reg_dir = os.path.join(repo_root, "Docs", "Governance", "registry", "capabilities")
    os.makedirs(reg_dir, exist_ok=True)
    
    # 1. Concept Registry (Liquidity, Zones, etc.)
    concept_entries = [
        {"name": "PDH", "subcategory": "Liquidity Objects"},
        {"name": "PDL", "subcategory": "Liquidity Objects"},
        {"name": "EQH", "subcategory": "Liquidity Objects"},
        {"name": "EQL", "subcategory": "Liquidity Objects"},
        {"name": "Sweep", "subcategory": "Liquidity Events"},
        {"name": "MSS", "subcategory": "Liquidity Events"},
        {"name": "CHOCH", "subcategory": "Liquidity Events"},
        {"name": "FVG", "subcategory": "Liquidity Footprints"},
        {"name": "Order Block", "subcategory": "Institutional Zones"},
        {"name": "Breaker Block", "subcategory": "Institutional Zones"},
        {"name": "Session High", "subcategory": "Context Concepts"},
    ]
    
    # 2. Methodology Registry (Families)
    meth_entries = [
        {"name": "Trend Following", "subcategory": "Directional"},
        {"name": "Momentum", "subcategory": "Velocity"},
        {"name": "Mean Reversion", "subcategory": "Statistical"},
        {"name": "ICT", "subcategory": "Institutional"},
        {"name": "Wyckoff", "subcategory": "Structural"},
        {"name": "Order Flow", "subcategory": "Microstructural"},
        {"name": "Volume Profile", "subcategory": "Auction"},
    ]
    
    # 3. Strategy Registry (Implementations)
    strat_entries = [
        {"name": "EMA Pullback", "subcategory": "Trend Following", "dependencies": ["Trend Following"]},
        {"name": "Donchian Breakout", "subcategory": "Breakout", "dependencies": ["Trend Following"]},
        {"name": "RSI-2", "subcategory": "Mean Reversion", "dependencies": ["Mean Reversion"]},
    ]
    
    # Write to files
    counter = 1
    
    def dump_reg(name, items, platform):
        nonlocal counter
        entries = []
        for i in items:
            entry = {
                "id": f"CAP-{counter:03d}",
                "name": i["name"],
                "category": name,
                "subcategory": i["subcategory"],
                "owner_platform": platform,
                "dependencies": i.get("dependencies", []),
                "implementation_state": "Planned",
                "frozen": False,
                "certified": False
            }
            entries.append(entry)
            counter += 1
        with open(os.path.join(reg_dir, f"{name.lower()}_registry.yaml"), "w") as f:
            yaml.dump({"entries": entries}, f, default_flow_style=False)
            
    dump_reg("concept", concept_entries, "Platform 9")
    dump_reg("methodology", meth_entries, "Platform 10")
    dump_reg("strategy", strat_entries, "Platform 11")
    
    print("Ontology generated.")

if __name__ == "__main__":
    generate_ontology(r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid")
