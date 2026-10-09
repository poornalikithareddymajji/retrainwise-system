import json
import os

class CostBenefitDecisionEngine:
    def __init__(self, pricing_config_path: str = None):
        # Base INR pricing parameters
        self.pricing = {
            "cpu_standard_hourly": 20.0,            # ~₹20/hr cloud compute
            "engineer_hourly_rate": 1200.0,         # ~₹1,200/hr engineer oversight
            "deployment_risk_penalty_base": 150.0   # ~₹150 base deployment risk
        }

    def evaluate(self, telemetry: dict, expected_sample_volume: int = 1000) -> dict:
        current_error_rate = telemetry.get("rolling_error_rate", 0.0)
        
        # Estimate value recovery directly in Indian Rupees (₹)
        projected_error_cost_inr = current_error_rate * expected_sample_volume * 10.0
        estimated_retrain_benefit_inr = projected_error_cost_inr * 0.75

        # Compute cost terms in INR (₹)
        compute_cost = 0.05 * self.pricing["cpu_standard_hourly"]
        human_cost = 0.1 * self.pricing["engineer_hourly_rate"]
        deploy_risk = self.pricing["deployment_risk_penalty_base"]
        full_retrain_cost_inr = compute_cost + human_cost + deploy_risk

        partial_update_cost_inr = (0.01 * self.pricing["cpu_standard_hourly"]) + 50.0

        net_full_retrain = estimated_retrain_benefit_inr - full_retrain_cost_inr
        net_partial_update = (estimated_retrain_benefit_inr * 0.5) - partial_update_cost_inr
        net_defer = 0.0

        candidates = {
            "RETRAIN_NOW": float(net_full_retrain),
            "PARTIAL_UPDATE": float(net_partial_update),
            "DEFER": float(net_defer)
        }

        recommended_action = max(candidates, key=candidates.get)

        return {
            "recommended_action": recommended_action,
            "expected_benefit_inr": float(estimated_retrain_benefit_inr),
            "expected_benefit_usd": float(estimated_retrain_benefit_inr / 83.0), # Backwards compatibility alias
            "full_retrain_cost_inr": float(full_retrain_cost_inr),
            "net_expected_value_inr": float(candidates[recommended_action]),
            "action_scores": candidates
        }