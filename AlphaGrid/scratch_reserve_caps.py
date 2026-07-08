import yaml
import os

CAPABILITIES_PATH = r"Docs\Governance\registry\capability_registry.yaml"
ONTOLOGY_PATH = r"Docs\Governance\registry\ontology_registry.yaml"

RESERVED = [
    # Auction/Market Profile
    {"id": "001", "name": "AuctionProfile", "desc": "Analyzes market profile and auction theory."},
    {"id": "002", "name": "InitialBalance", "desc": "Calculates the initial balance of the session."},
    {"id": "003", "name": "OpeningDrive", "desc": "Identifies opening drive momentum."},
    {"id": "004", "name": "ResponsiveBuyingSelling", "desc": "Identifies responsive market participation."},
    {"id": "005", "name": "InitiativeBuyingSelling", "desc": "Identifies initiative market participation."},
    {"id": "006", "name": "PoorHighLow", "desc": "Detects poor highs and lows."},
    {"id": "007", "name": "SinglePrints", "desc": "Detects single print zones."},
    {"id": "008", "name": "CompositeProfile", "desc": "Calculates composite volume profiles."},
    # Execution Microstructure
    {"id": "009", "name": "QueueImbalance", "desc": "Detects order book queue imbalance."},
    {"id": "010", "name": "Icebergs", "desc": "Detects iceberg orders."},
    {"id": "011", "name": "Spoofing", "desc": "Detects spoofing patterns."},
    {"id": "012", "name": "OrderBookPressure", "desc": "Measures total order book pressure."},
    # Options
    {"id": "013", "name": "GammaExposure", "desc": "Calculates GEX levels."},
    {"id": "014", "name": "DealerPositioning", "desc": "Estimates aggregate dealer positioning."},
    {"id": "015", "name": "IVRank", "desc": "Calculates Implied Volatility Rank."},
    {"id": "016", "name": "MaxPain", "desc": "Calculates option max pain levels."},
    # Macro
    {"id": "017", "name": "EconomicCalendar", "desc": "Ingests economic calendar events."},
    {"id": "018", "name": "CentralBankEvents", "desc": "Tracks central bank announcements."},
    {"id": "019", "name": "YieldCurve", "desc": "Analyzes yield curve spread changes."},
    # Statistical
    {"id": "020", "name": "HurstExponent", "desc": "Calculates the Hurst exponent for mean reversion/trending."},
    {"id": "021", "name": "Entropy", "desc": "Measures market entropy."},
    {"id": "022", "name": "Cointegration", "desc": "Analyzes asset cointegration."},
    {"id": "023", "name": "KalmanFilter", "desc": "Applies Kalman filtering for state estimation."},
    # AI
    {"id": "024", "name": "FeatureImportance", "desc": "Extracts real-time feature importance."},
    {"id": "025", "name": "SHAP", "desc": "Calculates SHAP values for model predictions."},
    {"id": "026", "name": "DriftDetection", "desc": "Detects concept drift in live models."}
]

def append_registry():
    with open(CAPABILITIES_PATH, "r") as f:
        caps = yaml.safe_load(f)

    with open(ONTOLOGY_PATH, "r") as f:
        onto = yaml.safe_load(f)

    for item in RESERVED:
        cap_id = f"CAP-RES-{item['id']}"
        ont_id = f"ONT-RES-{item['id']}"
        
        # Add Capability
        if not any(c.get("id") == cap_id for c in caps.get("entries", [])):
            if "entries" not in caps: caps["entries"] = []
            caps["entries"].append({
                "id": cap_id,
                "name": item["name"],
                "description": item["desc"],
                "domain": "Reserved",
                "tier": "Future",
                "status": "Backlog",
                "implementation_state": "Backlog",
                "blocking": False,
                "complexity": "Unknown"
            })
            
        # Add Ontology
        if not any(o.get("id") == ont_id for o in onto.get("entries", [])):
            if "entries" not in onto: onto["entries"] = []
            onto["entries"].append({
                "id": ont_id,
                "name": item["name"],
                "description": item["desc"],
                "domain": "Reserved",
                "relationships": []
            })

    with open(CAPABILITIES_PATH, "w") as f:
        yaml.dump(caps, f, sort_keys=False, default_flow_style=False)

    with open(ONTOLOGY_PATH, "w") as f:
        yaml.dump(onto, f, sort_keys=False, default_flow_style=False)
        
    print(f"Reserved {len(RESERVED)} capabilities and ontologies.")

if __name__ == "__main__":
    append_registry()
