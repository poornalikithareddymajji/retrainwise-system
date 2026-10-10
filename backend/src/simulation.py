# backend/src/simulation.py
import numpy as np
from typing import List, Dict, Any

class DriftSimulationHarness:
    """
    Injects synthetic feature drift and simulates time-series monitoring environments.
    """
    def __init__(self, n_timesteps: int = 50):
        self.n_timesteps = n_timesteps

    def run_simulation(self, drift_type: str = "sudden") -> List[Dict[str, Any]]:
        traces = []
        base_accuracy = 0.92

        for t in range(self.n_timesteps):
            # Inject artificial drift starting at timestep 20
            if t >= 20:
                if drift_type == "sudden":
                    accuracy_loss = 0.25
                elif drift_type == "gradual":
                    accuracy_loss = min(0.30, (t - 20) * 0.015)
                else:
                    accuracy_loss = 0.10 * np.sin(t / 5)
            else:
                accuracy_loss = 0.0

            current_accuracy = max(0.50, base_accuracy - accuracy_loss)
            p_value = float(np.exp(-accuracy_loss * 15)) + np.random.uniform(0.001, 0.02)
            compute_cost = 1500.0  # ₹1,500 base retraining cost
            loss_cost = accuracy_loss * 50000.0  # Business impact in INR

            traces.append({
                "timestep": t,
                "accuracy": round(current_accuracy, 4),
                "p_value": round(p_value, 4),
                "compute_cost_inr": compute_cost,
                "business_loss_inr": round(loss_cost, 2),
                "net_benefit_inr": round(loss_cost - compute_cost, 2)
            })

        return traces