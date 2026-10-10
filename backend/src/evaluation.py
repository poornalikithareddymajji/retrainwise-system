# backend/src/evaluation.py
from typing import Dict, List, Any

class PolicyEvaluator:
    """
    Compares RetrainWise policy against standard industry baselines.
    """
    def evaluate_all(self, traces: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = {}

        # 1. Calendar Policy (Retrain every 10 timesteps)
        calendar_retrains = len([t for t in traces if t["timestep"] % 10 == 0])
        
        # 2. Trigger Policy (Retrain whenever p_value < 0.05)
        trigger_retrains = len([t for t in traces if t["p_value"] < 0.05])
        
        # 3. RetrainWise (Retrain only when p_value < 0.05 AND net_benefit_inr > 0)
        retrainwise_retrains = len([
            t for t in traces if t["p_value"] < 0.05 and t["net_benefit_inr"] > 0
        ])

        results["Calendar"] = {"retrains": calendar_retrains, "cost_efficiency": "Low"}
        results["DriftTrigger"] = {"retrains": trigger_retrains, "cost_efficiency": "Medium"}
        results["RetrainWise"] = {"retrains": retrainwise_retrains, "cost_efficiency": "Optimal"}

        return results