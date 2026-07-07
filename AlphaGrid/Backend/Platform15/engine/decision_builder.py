from Backend.Platform15.contracts.dtos import RiskContextDTO, RiskAssessmentDTO, RiskReason
class DecisionBuilder:
    __version__ = 'v1.0'
    __dto_version__ = 'v1.0'
    __schema_version__ = 'v1.0'
    def build(self, recommendation, context: RiskContextDTO, engine_results: list, recommended_size: float) -> RiskAssessmentDTO:
        all_reasons = []
        has_fail = False
        has_warn = False
        
        for res in engine_results:
            if res.state == "FAIL":
                has_fail = True
            elif res.state == "WARNING":
                has_warn = True
            all_reasons.extend(res.reasons)
            
        decision = "ACCEPTED"
        if has_fail:
            decision = "REJECTED"
            recommended_size = 0.0
        elif has_warn:
            decision = "ACCEPTED_WITH_WARNINGS"
            
        max_downside = recommended_size * abs(recommendation.entry_price - recommendation.stop_loss)
        
        return RiskAssessmentDTO(
            recommendation_id=recommendation.id,
            decision=decision,
            recommended_position_size=recommended_size,
            max_downside_usd=max_downside,
            reasons=all_reasons
        )