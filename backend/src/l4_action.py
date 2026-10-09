from sklearn.linear_model import SGDClassifier
import numpy as np

class ActionExecutor:
    def __init__(self):
        self.model = SGDClassifier(loss="log_loss", random_state=42)
        self.is_fitted = False
        self.classes = np.array([0, 1])
        self.n_features = None

    def reset(self):
        self.model = SGDClassifier(loss="log_loss", random_state=42)
        self.is_fitted = False
        self.n_features = None

    def train_or_update(self, X: np.ndarray, y: np.ndarray):
        X = np.array(X)
        y = np.array(y)
        
        # If feature dimension changed, reset classifier
        if self.n_features is not None and X.shape[1] != self.n_features:
            self.reset()
            
        self.n_features = X.shape[1]
        
        if not self.is_fitted:
            self.model.partial_fit(X, y, classes=self.classes)
            self.is_fitted = True
        else:
            self.model.partial_fit(X, y)

    def predict(self, X: np.ndarray) -> int:
        X = np.array(X)
        if not self.is_fitted:
            return 0
        
        # Guard against feature mismatch during predictions
        if self.n_features is not None and X.shape[1] != self.n_features:
            self.reset()
            return 0

        return int(self.model.predict(X)[0])