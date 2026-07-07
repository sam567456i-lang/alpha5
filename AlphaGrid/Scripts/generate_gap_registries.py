import yaml
import os

GOVERNANCE_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry"

def generate_gap_registries():
    # 1. Engine Registry (The 24 missing pieces)
    engines = [
        {"id": "ENG_MARKET_UNIVERSE_SCANNER", "platform": "P03", "type": "Pre-Execution"},
        {"id": "ENG_OPPORTUNITY_SCANNER", "platform": "P14", "type": "Execution"},
        {"id": "ENG_MULTI_TIMEFRAME", "platform": "P06", "type": "Context"},
        {"id": "ENG_SESSION", "platform": "P06", "type": "Context"},
        {"id": "ENG_MARKET_REGIME", "platform": "P09", "type": "Context"},
        {"id": "ENG_DATA_AVAILABILITY", "platform": "P02", "type": "Pre-Execution"},
        {"id": "ENG_STRATEGY_PERFORMANCE_REGISTRY", "platform": "P27", "type": "Research"},
        {"id": "ENG_EVIDENCE_VOTING", "platform": "P15", "type": "Evaluation"},
        {"id": "ENG_OPPORTUNITY_LIFECYCLE", "platform": "P14", "type": "Execution"},
        {"id": "ENG_MONITORING", "platform": "P21", "type": "Monitoring"},
        {"id": "ENG_DASHBOARD_QUERY", "platform": "P21", "type": "Monitoring"},
        {"id": "ENG_AI_AGENT_NETWORK", "platform": "P30", "type": "AI"},
        {"id": "ENG_KNOWLEDGE_GRAPH", "platform": "P30", "type": "AI"},
        {"id": "ENG_RESEARCH_PIPELINE", "platform": "P24", "type": "Research"},
        {"id": "ENG_EXTERNAL_REPOSITORY", "platform": "P29", "type": "Integration"},
        {"id": "ENG_HISTORICAL_PATTERN_LIBRARY", "platform": "P27", "type": "Research"},
        {"id": "ENG_CONFIDENCE_CALIBRATION", "platform": "P16", "type": "Evaluation"},
        {"id": "ENG_CONTINUOUS_LEARNING", "platform": "P28", "type": "Research"},
        {"id": "ENG_EXPLAINABILITY_CONTRACT", "platform": "P15", "type": "Evaluation"},
        {"id": "ENG_OPPORTUNITY_RANKING", "platform": "P17", "type": "Ranking"},
        {"id": "ENG_SCORING", "platform": "P15", "type": "Evaluation"},
        {"id": "ENG_REALTIME_INCREMENTAL_EXEC", "platform": "P10", "type": "Execution"}
    ]
    
    with open(os.path.join(GOVERNANCE_DIR, "engine_registry.yaml"), "w") as f:
        yaml.dump({"engines": engines}, f, sort_keys=False)
        
    # 2. Detailed Methodology Registry
    methodologies = {
        "ICT": ["2022_Model", "2023_Model", "Silver_Bullet", "OTE", "Unicorn"],
        "SMC": ["BOS_Continuation", "OB_Reversal", "FVG_Mitigation"],
        "Wyckoff": ["Spring", "LPS", "Sign_of_Strength"],
        "Trend": ["EMA_Pullback", "Donchian_Breakout"],
        "Breakout": ["ORB", "NR7"],
        "VWAP": ["Mean_Reversion"],
        "Quant": ["Kalman_Filter", "Cointegration"]
    }
    
    methodology_records = []
    for family, strategies in methodologies.items():
        for strat in strategies:
            methodology_records.append({
                "methodology_id": f"METH_{family.upper()}_{strat.upper()}",
                "family": family,
                "name": strat.replace("_", " "),
                "platform": "P12",
                "maturity": "planned"
            })
            
    with open(os.path.join(GOVERNANCE_DIR, "methodology_registry.yaml"), "w") as f:
        yaml.dump({"methodologies": methodology_records}, f, sort_keys=False)
        
    # 3. Market Suitability Matrix
    suitability = {
        "markets": ["NSE_Index_Options", "NSE_Futures", "NSE_Cash"],
        "timeframes": ["1m", "5m", "15m", "1H", "4H", "1D"],
        "styles": ["Scalp", "Intraday", "Swing", "Position"],
        "sessions": ["Asian", "London", "New York", "India"],
        "regimes": ["Trending", "Ranging", "High Volatility", "Low Volatility"]
    }
    
    with open(os.path.join(GOVERNANCE_DIR, "market_suitability_matrix.yaml"), "w") as f:
        yaml.dump({"suitability_matrix": suitability}, f, sort_keys=False)

if __name__ == "__main__":
    generate_gap_registries()
    print("Gap Registries Successfully Generated.")
