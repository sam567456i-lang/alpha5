from typing import Dict, List, Any

class DomainRegistry:
    """Master ownership table for all Platform 10 domains."""
    def __init__(self):
        self.domains: Dict[str, Dict[str, Any]] = {
            "Market Structure": {"owner": "core_team", "capabilities": []},
            "Liquidity": {"owner": "core_team", "capabilities": []},
            "Auction": {"owner": "core_team", "capabilities": []},
            "Volume": {"owner": "core_team", "capabilities": []},
            "Cross Market": {"owner": "core_team", "capabilities": []},
            "Time": {"owner": "core_team", "capabilities": []},
            "Statistics": {"owner": "core_team", "capabilities": []},
            "Order Flow": {"owner": "core_team", "capabilities": []},
            "Price Action": {"owner": "core_team", "capabilities": []}
        }
        
    def register_capability(self, domain: str, capability_name: str):
        if domain not in self.domains:
            raise ValueError(f"Unknown domain: {domain}")
        self.domains[domain]["capabilities"].append(capability_name)
