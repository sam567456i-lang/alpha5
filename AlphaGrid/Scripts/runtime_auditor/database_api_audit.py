import json
import logging
import os

logger = logging.getLogger("RuntimeAuditor.DatabaseAPIAudit")

class APITracer:
    """Traces Endpoint -> Router -> Service -> Pipeline -> Registry -> Database."""
    
    def __init__(self):
        self.endpoint_traces = []

    def log_trace(self, endpoint: str, service: str, registries_hit: list):
        self.endpoint_traces.append({
            "endpoint": endpoint,
            "service_invoked": service,
            "registries_hit": registries_hit
        })

    def export(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "api_execution_graph.json"), "w") as f:
            json.dump({"traces": self.endpoint_traces}, f, indent=2)

