import yaml
import os
import uuid

GOVERNANCE_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\registry"

def create_base_metadata():
    return {
        "supported_markets": ["all"],
        "supported_assets": ["all"],
        "supported_sessions": ["all"],
        "supported_timeframes": ["all"],
        "supported_styles": ["all"],
        "supported_methodologies": ["all"],
        "required_data": [],
        "required_indicators": [],
        "required_analyses": [],
        "required_features": [],
        "required_concepts": [],
        "required_validators": [],
        "required_dashboard_widgets": [],
        "required_ai_agents": [],
        "streaming_support": True,
        "cache_support": True,
        "incremental_support": True,
        "performance_profile": "O(N)",
        "maturity": "research",
        "implementation_status": "planned"
    }

def create_strategy_performance():
    return {
        "win_rate": 0.0,
        "profit_factor": 0.0,
        "expectancy": 0.0,
        "average_rr": 0.0,
        "best_markets": [],
        "best_timeframes": [],
        "best_sessions": [],
        "best_regimes": [],
        "known_weaknesses": []
    }

def generate_analysis_registry():
    families = {
        "Market Context": ["Regime", "Trend vs Range", "Liquidity Regime", "Sector Rotation", "Cross Market Context"],
        "Technical": ["SMA", "EMA", "ATR", "ADX", "MACD", "RSI", "ROC", "Donchian", "Keltner", "Supertrend", "Ichimoku", "Parabolic SAR"],
        "Price Action": ["Swing Structure", "Higher High", "Higher Low", "Lower High", "Lower Low", "Compression", "Expansion", "Break Retest", "False Break", "Channels", "Trendlines", "Range", "Opening Range", "NR4", "NR7"],
        "Candlestick": ["Pin Bar", "Engulfing", "Hammer", "Morning Star", "Doji", "Harami"],
        "Pattern Recognition": ["Triangle", "Wedge", "Flag", "Pennant", "Rectangle", "Cup Handle", "Double Top", "Head & Shoulders"],
        "Market Structure": ["BOS", "CHoCH", "MSS", "Internal Structure", "External Structure", "Protected High", "Protected Low"],
        "Smart Money Concepts": ["Order Block", "Breaker", "Mitigation", "Rejection Block", "Propulsion Block", "FVG", "IFVG", "BPR", "Consequent Encroachment", "Liquidity Void", "Displacement", "Premium", "Discount", "OTE", "Power of Three", "SMT"],
        "Liquidity": ["PDH", "PDL", "PWH", "PWL", "PMH", "PML", "EQH", "EQL", "Liquidity Pools", "Stop Clusters", "Liquidity Sweep", "Liquidity Grab", "Stop Hunt", "Failed Auction"],
        "Supply Demand": ["Supply Zones", "Demand Zones", "Fresh Zones", "Zone Quality", "Zone Age", "Zone Strength", "Reaction Probability"],
        "Volume": ["VWAP", "Anchored VWAP", "OBV", "A/D", "CMF", "Volume Delta", "Relative Volume", "Volume Spike", "Volume Dry Up", "Effort vs Result"],
        "Volume Profile": ["POC", "VAH", "VAL", "HVN", "LVN", "Naked POC", "Developing POC"],
        "Market Profile": ["Initial Balance", "Single Prints", "Poor High", "Poor Low", "Double Distribution", "P Shape", "B Shape", "Excess"],
        "Order Flow": ["Footprint", "CVD", "Icebergs", "Absorption", "Exhaustion", "Queue", "Large Orders"],
        "Order Book": ["Depth", "Liquidity Walls", "Spoofing", "Stacking", "Pulling", "Sweep Orders"],
        "Tape Reading": ["Time & Sales", "Large Prints", "Aggressive Buyers", "Aggressive Sellers", "Tape Speed"],
        "Futures": ["Open Interest", "Long Build Up", "Short Build Up", "Long Unwinding", "Short Covering", "Basis", "Contango", "Backwardation"],
        "Options": ["Gamma", "Dealer Position", "Gamma Flip", "Call Wall", "Put Wall", "Max Pain", "Open Interest"],
        "Fundamental": ["Revenue", "EPS", "Margins", "Cash Flow", "Debt", "ROE", "ROCE", "Valuation", "Management"],
        "Macro": ["GDP", "Inflation", "Interest Rates", "Central Banks", "Employment", "PMI", "Fiscal Policy"],
        "Economic Events": ["FOMC", "NFP", "CPI", "PPI", "Retail Sales", "Earnings"],
        "Sentiment": ["News", "Social", "Fear & Greed", "Analyst Ratings", "Funding"],
        "Breadth": ["Advance Decline", "TRIN", "Tick", "Market Breadth", "Participation"],
        "Relative Strength": ["Sector", "Industry", "Cross Asset", "Relative Weakness", "Rotation"],
        "Correlation": ["Rolling Correlation", "Lead Lag", "Cointegration", "Cross Market"],
        "Intermarket": ["General Intermarket"],
        "Seasonal": ["Month End", "Quarter End", "Holiday", "Election", "Harvest"],
        "Cycles": ["Market Cycle", "Business Cycle", "Volatility Cycle", "Dominant Cycle"],
        "Statistical": ["Z Score", "Percentile", "Entropy", "Fractal Dimension", "Hurst", "Autocorrelation", "Monte Carlo", "Bayesian"],
        "Quantitative": ["General Quantitative"],
        "Machine Learning": ["Regime Classification", "Pattern Classification", "Anomaly Detection", "Meta Labels", "Feature Importance", "Embeddings", "HMM"],
        "Portfolio Analytics": ["Correlation", "Exposure", "Diversification", "Heat", "Sharpe", "Sortino", "Calmar", "Kelly"],
        "Execution Analytics": ["Spread", "Slippage", "Latency", "Execution Cost", "Market Impact", "Liquidity Availability"]
    }
    
    registry = {"analyses": []}
    for family, caps in families.items():
        for cap in caps:
            cid = f"ANA_{family.upper().replace(' ', '_')}_{cap.upper().replace(' ', '_')}"
            entry = {
                "capability_id": cid,
                "name": cap,
                "platform": "P06_Analysis",
                "family": family,
                **create_base_metadata()
            }
            if family in ["Order Flow", "Tape Reading"]:
                entry["required_data"].append("Tick")
            if family == "Order Book":
                entry["required_data"].append("Level 2")
            if family == "Options":
                entry["required_data"].append("Options Chain")
            if family in ["Macro", "Economic Events"]:
                entry["required_data"].append("Economic Calendar")
            registry["analyses"].append(entry)
            
    with open(os.path.join(GOVERNANCE_DIR, "analysis_registry.yaml"), "w") as f:
        yaml.dump(registry, f, sort_keys=False)
        
def generate_methodology_and_strategies():
    methodologies = {
        "ICT": ["2022 Model", "2023 Model", "OTE", "Silver Bullet", "Unicorn", "Judas Swing"],
        "Smart Money Concepts": ["Liquidity Sweep", "FVG", "Order Block", "Breaker", "Mitigation"],
        "Wyckoff": ["Spring", "Upthrust", "SOS", "SOW", "LPS", "LPSY"],
        "Trend Following": ["EMA Pullback", "Donchian Breakout", "Turtle", "Supertrend"],
        "Breakout Trading": ["ORB", "Volatility Breakout", "NR7"],
        "Mean Reversion": ["VWAP Reversion", "Bollinger", "RSI Extremes", "Regression"],
        "Auction Market Theory": ["Value Area Play"],
        "Volume Spread Analysis": ["No Demand", "No Supply"],
        "Statistical Arbitrage": ["Pairs Trading", "Cointegration Reversion"],
        "Quantitative": ["Kalman Filter Momentum"]
    }
    
    meth_registry = {"methodologies": []}
    strat_registry = {"strategies": []}
    
    for meth, strats in methodologies.items():
        mid = f"METH_{meth.upper().replace(' ', '_')}"
        meth_entry = {
            "methodology_id": mid,
            "name": meth,
            "platform": "P12_Methodology",
            **create_base_metadata()
        }
        meth_registry["methodologies"].append(meth_entry)
        
        for strat in strats:
            sid = f"STRAT_{meth.upper().replace(' ', '_')}_{strat.upper().replace(' ', '_')}"
            strat_entry = {
                "strategy_id": sid,
                "name": strat,
                "parent_methodology": mid,
                "platform": "P12_Methodology",
                **create_base_metadata(),
                "performance_metrics": create_strategy_performance()
            }
            strat_registry["strategies"].append(strat_entry)
            
    with open(os.path.join(GOVERNANCE_DIR, "methodology_registry.yaml"), "w") as f:
        yaml.dump(meth_registry, f, sort_keys=False)
        
    with open(os.path.join(GOVERNANCE_DIR, "strategy_registry.yaml"), "w") as f:
        yaml.dump(strat_registry, f, sort_keys=False)

if __name__ == "__main__":
    generate_analysis_registry()
    generate_methodology_and_strategies()
    print("Capability Registries Mass-Generated successfully.")
