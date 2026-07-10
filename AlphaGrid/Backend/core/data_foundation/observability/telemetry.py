from typing import Dict, Any

class TelemetryEngine:
    """Institutional observability tracking for ingestion and validation pipelines."""
    
    @staticmethod
    def log_ingestion_metrics(adapter_name: str, records_processed: int, elapsed_time_ms: float):
        throughput = records_processed / (elapsed_time_ms / 1000.0) if elapsed_time_ms > 0 else 0
        print(f"[METRIC] Adapter: {adapter_name} | Throughput: {throughput:.2f} rows/sec")
        
    @staticmethod
    def trigger_alert(severity: str, message: str):
        print(f"[ALERT - {severity}] {message}")
