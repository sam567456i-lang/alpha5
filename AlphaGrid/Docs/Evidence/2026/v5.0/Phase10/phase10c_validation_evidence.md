---
Document ID: EVID-002
Title: "Phase 10 Cycle 3 Validation Evidence"
Version: 1.0.0
Governance Version: 1.0.0
Architecture Version: 1.0.0
Phase: 10
Owner: ArchitectureTeam
Category: Evidence
Maturity: "Level 5: Institutionally Frozen"
Implementation Status: Validated
Current Phase: 10
Future Phase: N/A
Last Validated Phase: 10
Review Date: 2026-07-03
Dependencies: []
Referenced By: []
---

# Phase 10 Cycle 3 Validation Evidence

This artifact preserves the raw console outputs generated during the institutional validation of the Breakout Family.

## 1. End-to-End Execution, Stress Test, and Deterministic Replay
Command: `python run_breakout_validation.py`

```text
=========================================
1. END-TO-END PIPELINE & DTO CAPTURE
=========================================

--- FeatureDTO ---
{
  "id": "ftr-volbreakout-14-1.5-dd2b9003",
  "schema_version": "1.0.0",
  "owner": "Feature",
  "producer": "ftr-volbreakout-14-1.5",
  "created_at": "2026-07-03 17:01:59.793569",
  "updated_at": "2026-07-03 17:01:59.793569",
  "trace_id": "trace-e2e-1",
  "correlation_id": "cor-1",
  "fingerprint": "volbreakout-14-1.5",
  "checksum": "dd3f0eb8b73ab39833199cf432f5b330",
  "quality": 1.0,
  "confidence": 0.95,
  "lifecycle": "ACTIVE",
  "tags": [],
  "lineage": {
    "dependencies": [
      "ftr-ohlcv",
      "ftr-atr-14"
    ]
  },
  "symbol": "TEST/USD",
  "timeframe": "1m",
  "values": {
    "atr": 21.582457303921267,
    "upper_threshold": 142.39110731171183,
    "lower_threshold": 77.64373539994806,
    "upside_breakout": false,
    "downside_breakout": false
  }
}

--- ConceptDTO ---
{
  "id": "con-breakout-6e8a006c",
  "schema_version": "1.0.0",
  "owner": "Concept",
  "producer": "con-breakout",
  "created_at": "2026-07-03 17:01:59.793569",
  "updated_at": "2026-07-03 17:01:59.793569",
  "trace_id": "trace-e2e-1",
  "correlation_id": "cor-1",
  "fingerprint": "breakout-concept",
  "checksum": "d3479191a881b436e3020e419b1eeabd",
  "quality": 1.0,
  "confidence": 0.95,
  "lifecycle": "ACTIVE",
  "tags": [],
  "lineage": {
    "dependencies": [
      "ftr-volbreakout-14-1.5-dd2b9003"
    ]
  },
  "concept_type": "BREAKOUT",
  "state": "CONTAINED",
  "metadata": {
    "bullish_signals": 0,
    "bearish_signals": 0
  }
}

--- MethodologyDTO ---
{
  "id": "meth-breakout-2c26dbc4",
  "schema_version": "1.0.0",
  "owner": "Methodology",
  "producer": "meth-breakout",
  "created_at": "2026-07-03 17:01:59.793569",
  "updated_at": "2026-07-03 17:01:59.793569",
  "trace_id": "trace-e2e-1",
  "correlation_id": "cor-1",
  "fingerprint": "breakout-methodology",
  "checksum": "e4710344ed1365cca226b80eea00ab79",
  "quality": 1.0,
  "confidence": 0.95,
  "lifecycle": "ACTIVE",
  "tags": [],
  "lineage": {
    "dependencies": [
      "con-breakout-6e8a006c"
    ]
  },
  "is_active": false,
  "direction": 0,
  "metadata": {
    "trend_aligned": false,
    "breakout_state": "CONTAINED"
  }
}

--- SignalDTO ---
{
  "id": "sig-gen-breakout-281fc920",
  "schema_version": "1.0.0",
  "owner": "Signal",
  "producer": "sig-gen-breakout",
  "created_at": "2026-07-03 17:01:59.794567",
  "updated_at": "2026-07-03 17:01:59.794567",
  "trace_id": "trace-e2e-1",
  "correlation_id": "cor-1",
  "fingerprint": "sig-breakout",
  "checksum": "8d072c85a8917c2c1dcafd5e309ded5a",
  "quality": 1.0,
  "confidence": 0.0,
  "lifecycle": "ACTIVE",
  "tags": [],
  "lineage": {
    "dependencies": [
      "meth-breakout-2c26dbc4"
    ]
  }
}

--- StrategyDTO ---
{
  "id": "strat-volbreakout-769ea58a",
  "schema_version": "1.0.0",
  "owner": "Strategy",
  "producer": "strat-volbreakout",
  "created_at": "2026-07-03 17:01:59.794567",
  "updated_at": "2026-07-03 17:01:59.794567",
  "trace_id": "trace-e2e-1",
  "correlation_id": "cor-1",
  "fingerprint": "strat-volbreakout-base",
  "checksum": "0bc90450a3c014f6a6ef2b83c9201e8f",
  "quality": 1.0,
  "confidence": 0.95,
  "lifecycle": "ACTIVE",
  "tags": [],
  "lineage": {
    "dependencies": [
      "sig-gen-breakout-281fc920"
    ]
  },
  "action": "HOLD",
  "metadata": {
    "parameters_used": {
      "atr_period": 14,
      "multiplier": 1.5
    },
    "strategy_metadata": {
      "id": "strat-volbreakout",
      "family": "Breakout",
      "methodology": "meth-breakout",
      "required_features": [
        "ftr-volbreakout-14-1.5"
      ],
      "required_geometry": [],
      "required_concepts": [
        "con-breakout"
      ],
      "required_methodologies": [
        "meth-breakout"
      ],
      "required_signals": [
        "sig-gen-breakout"
      ],
      "supported_markets": [
        "Stocks",
        "Crypto",
        "Forex",
        "Futures"
      ],
      "supported_timeframes": [
        "15m",
        "1h",
        "4h"
      ],
      "supported_styles": [
        "Scalping",
        "Intraday"
      ],
      "supported_sessions": [
        "ALL"
      ],
      "minimum_history": 42,
      "warmup_period": 14,
      "parameter_space_version": "1.0.0",
      "strategy_version": "0.1.0",
      "version": "0.1.0"
    }
  }
}

=========================================
2. STRESS TEST, PERFORMANCE & MEMORY
=========================================
Dataset Size: 100,000 bars
Hardware CPU Count: 4
Elapsed Time: 0.0362 seconds
CPU Time: 0.0312 seconds
Peak RSS Before: 89.86 MB
Peak RSS After: 89.85 MB
Peak Memory Overhead: -0.01 MB

=========================================
3. DETERMINISTIC REPLAY (SHA256)
=========================================
Run 1 SHA256: 4068859b5ef8a8439d76fef367ccd6208c1feccf37ce8f6b49d3b905b44782d3
Run 2 SHA256: 4068859b5ef8a8439d76fef367ccd6208c1feccf37ce8f6b49d3b905b44782d3
Match: True
```

## 2. Registry Health Audit
Command: `python validate_registry.py`

```text
=========================================
CAPABILITY REGISTRY HEALTH AUDIT
=========================================

1. Duplicate Registrations: 0

2. Non-Strategy Orphan Capabilities: 46
   Details: ['ftr-candlebody', 'ftr-upperwick', 'ftr-lowerwick', 'ftr-bodyratio', 'geo-pivot', 'geo-swing', 'geo-range', 'geo-channel', 'con-momentum', 'con-liquidity', 'con-structure', 'meth-trendfollowing', 'meth-meanreversion', 'meth-smc', 'meth-wyckoff', 'strat-canonicalvalidation', 'strat-macdtrend', 'strat-smacross', 'strat-supertrend', 'strat-ichimoku', 'strat-rsireversion', 'int-macro', 'int-breadth', 'int-calendar', 'int-ownership', 'ftr-breadth', 'ftr-rs', 'ftr-currency', 'ftr-linreg', 'ftr-kama', 'ftr-hma', 'ftr-ichimoku', 'con-breadth', 'con-rs', 'con-seasonality', 'meth-breadth', 'meth-rs', 'meth-currency', 'meth-seasonal', 'ftr-rsi', 'ftr-bollinger', 'ftr-stochastic', 'ftr-vwap', 'ftr-keltner', 'con-extremum', 'sig-meanreversion']

3. Circular Dependencies Found: False

Total Capabilities Validated: 58
```

## 3. Repository Regression Tests
Command: `python -m pytest Tests/ -v`

```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-8.4.1, pluggy-1.6.0 -- C:\Program Files\Python311\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\praka\.gemini\antigravity\scratch\AlphaGrid
plugins: anyio-4.10.0, dash-3.2.0, langsmith-0.4.21, typeguard-4.4.4
collecting ... collected 15 items

Tests/test_breakout.py::test_sr_determinism PASSED                       [  6%]
Tests/test_breakout.py::test_hl_breakout_determinism PASSED              [ 13%]
Tests/test_breakout.py::test_vol_breakout_determinism PASSED             [ 20%]
Tests/test_breakout.py::test_breakout_concept_determinism PASSED         [ 26%]
Tests/test_breakout.py::test_breakout_methodology_determinism PASSED     [ 33%]
Tests/test_breakout.py::test_breakout_signal_determinism PASSED          [ 40%]
Tests/test_breakout.py::test_full_breakout_pipeline PASSED               [ 46%]
Tests/test_features_math.py::test_rsi_determinism PASSED                 [ 53%]
Tests/test_features_math.py::test_bollinger_determinism PASSED           [ 60%]
Tests/test_features_math.py::test_stochastic_determinism PASSED          [ 66%]
Tests/test_features_math.py::test_keltner_determinism PASSED             [ 73%]
Tests/test_features_math.py::test_vwap_determinism PASSED                [ 80%]
Tests/test_governance_breakout.py::test_explicit_deterministic_replay PASSED [ 86%]
Tests/test_governance_breakout.py::test_numerical_stability PASSED       [ 93%]
Tests/test_governance_breakout.py::test_performance_and_memory_budget PASSED [100%]

============================= 15 passed in 1.85s ==============================
```
