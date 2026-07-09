from Backend.core.interfaces.core_interfaces import ICapabilityScheduler, IResourceManager, ITelemetry
from Backend.core.execution_planner import ExecutionPlan

class ExecutionRuntime:
    """
    Orchestrates the execution lifecycle. Explicitly separates ordering (Scheduler),
    budgets (ResourceManager), and observability (Telemetry).
    """
    def __init__(self, scheduler: ICapabilityScheduler, resource_manager: IResourceManager, telemetry: ITelemetry):
        self.scheduler = scheduler
        self.resource_manager = resource_manager
        self.telemetry = telemetry
        
    def execute(self, plan: ExecutionPlan):
        self.telemetry.emit_metric("execution.start", 1.0, {"plan_id": plan.plan_id})
        
        # 1. Allocate baseline resources
        self.resource_manager.allocate("runtime_core", 512, 100)
        
        # 2. Hand off to scheduler to process the DAG
        self.scheduler.schedule(plan)
        
        # 3. Cleanup
        self.resource_manager.release("runtime_core")
        self.telemetry.emit_metric("execution.complete", 1.0, {"plan_id": plan.plan_id})
