from Backend.core.interfaces.core_interfaces import ICapabilityScheduler
from Backend.core.execution_planner import ExecutionPlan

class CapabilityScheduler(ICapabilityScheduler):
    """
    Schedules capabilities for execution strictly based on the provided ExecutionPlan DAG.
    """
    def schedule(self, execution_plan: ExecutionPlan):
        print(f"Scheduling execution plan: {execution_plan.plan_id}")
        for capability in execution_plan.capability_order:
            print(f"Dispatching: {capability}")
