class AgenticOrchestrator:
    def __init__(self, decision_engine):
        self.decision_engine = decision_engine

    def run_agent_loop(self, telemetry: dict) -> dict:
        decision = self.decision_engine.evaluate(telemetry)
        action = decision["recommended_action"]
        benefit = decision["expected_benefit_inr"]
        cost = decision["full_retrain_cost_inr"]

        staleness = telemetry.get("staleness_score", 0.0)
        error_rate = telemetry.get("rolling_error_rate", 0.0)

        if action == "RETRAIN_NOW":
            justification = (
                f"[TRIGGER: HIGH LEARNING DEBT / DRIFT]\n"
                f"Rolling Error Rate = {error_rate:.1%}, Staleness = {staleness:.2f}.\n"
                f"Expected Benefit (₹{benefit:.2f}) exceeds Full Retrain Cost (₹{cost:.2f}).\n"
                f"RECOMMENDATION: Executive action RETRAIN_NOW approved."
            )
        elif action == "PARTIAL_UPDATE":
            justification = (
                f"[TRIGGER: MODERATE DEGRADATION]\n"
                f"Rolling Error Rate = {error_rate:.1%}, Staleness = {staleness:.2f}.\n"
                f"Partial update balances performance recovery with lower compute overhead.\n"
                f"RECOMMENDATION: Execute PARTIAL_UPDATE (Incremental SGD step)."
            )
        else:
            justification = (
                f"[STATUS: NOMINAL OPERATION]\n"
                f"Rolling Error Rate = {error_rate:.1%}, Staleness = {staleness:.2f}.\n"
                f"Retrain benefit (₹{benefit:.2f}) does not outweigh execution cost (₹{cost:.2f}).\n"
                f"RECOMMENDATION: DEFER retraining. Continuing stream monitoring."
            )

        return {
            "telemetry": telemetry,
            "decision": decision,
            "agent_justification": justification
        }