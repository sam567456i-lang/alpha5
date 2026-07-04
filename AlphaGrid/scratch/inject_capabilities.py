import yaml

new_capabilities = [
    "Analysis Core", "Trend", "Momentum", "Volatility", "Support/Resistance", "Volume", 
    "Price Action", "Candlestick", "Chart Patterns", "Market Structure", "Smart Money", 
    "Liquidity", "Market Profile", "Order Flow", "Quantitative", "Statistical", 
    "Relative Strength", "Breadth", "Correlation", "Intermarket", "Macro", "Seasonal", 
    "Fundamental", "Sentiment", "Options", "Machine Learning", "AI Analysis", "External Analysis"
]

with open("master_capability_registry.yaml", "r") as f:
    data = yaml.safe_load(f)

for i, cap in enumerate(new_capabilities):
    # Formulate ID
    id_name = cap.replace(" ", "").replace("/", "").upper()
    cap_id = f"AN-{id_name}-{str(i+1).zfill(3)}"
    
    new_entry = {
        "id": cap_id,
        "category": "Analysis Platform",
        "family": cap,
        "name": f"{cap} Analysis",
        "owner": "ArchitectureTeam",
        "produces": ["AnalysisResult"],
        "consumes": ["Market Data", "Indicators"],
        "version": "1.0.0",
        "architecture_status": "approved",
        "implementation_status": "planned",
        "depends_on": [],
        "shared_component": True,
        "owner_layer": "Analysis",
        "lifecycle_state": "Planned",
        "stability": "Prototype",
        "used_by": ["Concept Engine", "Dashboard", "AI"],
        "supported_markets": ["Stocks", "Crypto", "Forex", "Futures"],
        "supported_timeframes": ["1m", "5m", "15m", "1h", "4h", "1d"],
        "supported_styles": ["Scalping", "Intraday", "Swing", "Position"],
        "supported_data": ["OHLCV"],
        "activation": {
            "enabled": True,
            "required_phase": 5,
            "required_family": cap,
            "required_dependencies": [],
            "required_switches": [],
            "minimum_version": "1.0.0",
            "maximum_version": None,
            "activation_policy": "Auto",
            "deactivation_policy": "Graceful",
            "requires": [],
            "optional_requires": [],
            "conflicts_with": []
        }
    }
    data["capabilities"].append(new_entry)

with open("master_capability_registry.yaml", "w") as f:
    yaml.dump(data, f, sort_keys=False, default_flow_style=False)

print("Injected 28 new capabilities into master_capability_registry.yaml")
