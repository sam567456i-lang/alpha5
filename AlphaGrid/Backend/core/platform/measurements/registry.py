from typing import Dict, Any

class MeasurementRegistry:
    """
    Metadata Registry for Platform 10 measurements.
    Declares the stable public API and capabilities.
    Does NOT instantiate or locate services. Orchestration must happen via Dependency Injection.
    """
    
    CATALOG = {
        "Pivot": {
            "type": "object",
            "causality": "OFFLINE",
            "schema_version": "1.0.0",
            "description": "Local extrema.",
            "inputs": {"lookback": "int", "lookforward": "int", "pivot_type": "HIGH|LOW"},
            "outputs": ["formation_bar", "timestamp", "price", "type", "provenance"],
            "algorithm_ids": ["CENTERED_N_BAR", "ZIGZAG", "FRACTAL"]
        },
        "Bar": {
            "type": "object",
            "causality": "ONLINE",
            "version": "1.0",
            "description": "OHLC entity.",
            "inputs": {},
            "outputs": ["bar_index", "timestamp", "open", "high", "low", "close", "provenance"]
        },
        "Touch": {
            "type": "event",
            "causality": "ONLINE",
            "version": "1.0",
            "description": "Raw interaction with a reference price.",
            "inputs": {"reference_price": "float"},
            "outputs": ["event_type", "bar_index", "timestamp", "observed_high", "observed_low", "reference_price", "provenance"]
        },
        "Cross": {
            "type": "event",
            "causality": "ONLINE",
            "version": "1.0",
            "description": "Price traversing a reference price.",
            "inputs": {"reference_price": "float"},
            "outputs": ["event_type", "direction", "previous_relation", "current_relation", "bar_index", "timestamp", "observed_price", "reference_price", "provenance"]
        },
        "ATR": {
            "type": "feature",
            "causality": "ONLINE",
            "version": "1.0",
            "description": "Average True Range.",
            "inputs": {"period": "int"},
            "outputs": ["bar_index", "timestamp", "value", "period", "provenance"]
        }
    }
    
    @classmethod
    def get_metadata(cls, measurement_name: str) -> Dict[str, Any]:
        if measurement_name not in cls.CATALOG:
            raise KeyError(f"Measurement {measurement_name} not found in public API registry.")
        return cls.CATALOG[measurement_name]
