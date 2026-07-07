from typing import Dict, Any
from Backend.Platform13.contracts.dtos import EvaluatedOpportunityDTO, QueueStatus
from Backend.Platform13.plugins.base import AbstractLifecyclePlugin

class OpportunityQueueManager(AbstractLifecyclePlugin):
    @property
    def plugin_id(self) -> str:
        return "plugin_queue_manager"

    def manage_lifecycle(self, dto: EvaluatedOpportunityDTO, policy: Dict[str, Any]) -> None:
        if dto.queue_status == QueueStatus.CANDIDATE:
            if dto.composite_opportunity_score >= policy.get("promotion_threshold", 0.8):
                dto.queue_status = QueueStatus.ACTIVE
            else:
                dto.queue_status = QueueStatus.QUEUED
        
        dto.evaluation_trace[self.plugin_id] = f"Queue status transitioned to {dto.queue_status.value}."
