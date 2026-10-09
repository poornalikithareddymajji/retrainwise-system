import numpy as np
from river import drift

class DriftAndStalenessMonitor:
    def __init__(self, delta=0.002):
        self.adwin = drift.ADWIN(delta=delta)
        self.total_predictions = 0
        self.steps_since_last_retrain = 0
        self.rolling_errors = []
        self.window_size = 100

    def update(self, y_true: int, y_pred: int) -> dict:
        self.total_predictions += 1
        self.steps_since_last_retrain += 1
        
        is_error = 1 if y_true != y_pred else 0
        self.adwin.update(is_error)
        self.rolling_errors.append(is_error)
        
        if len(self.rolling_errors) > self.window_size:
            self.rolling_errors.pop(0)

        drift_detected = self.adwin.drift_detected
        current_error_rate = float(np.mean(self.rolling_errors)) if self.rolling_errors else 0.0
        
        # Staleness score / Learning Debt state estimation
        staleness_score = float(current_error_rate * np.log1p(self.steps_since_last_retrain))

        return {
            "drift_detected": drift_detected,
            "rolling_error_rate": current_error_rate,
            "steps_since_retrain": self.steps_since_last_retrain,
            "staleness_score": staleness_score
        }

    def reset(self):
        self.steps_since_last_retrain = 0
        self.rolling_errors.clear()