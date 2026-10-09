import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

class StreamDatasetManager:
    def __init__(self):
        self.datasets = {}
        self.active_dataset_name = None
        self.current_index = 0
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
        self._load_default_benchmarks()

    def _load_default_benchmarks(self):
        # 1. Electricity (Elec2) Benchmark Stream
        np.random.seed(42)
        elec_X = np.random.randn(1000, 4)
        elec_y = (elec_X[:, 0] * 1.5 + elec_X[:, 1] > 0).astype(int)
        elec_df = pd.DataFrame(elec_X, columns=[f"feature_{i}" for i in range(4)])
        elec_df["target"] = elec_y

        # 2. Airlines Delay Stream
        air_X = np.random.randn(1000, 5)
        air_y = (air_X[:, 2] - air_X[:, 3] > 0.2).astype(int)
        air_df = pd.DataFrame(air_X, columns=[f"feature_{i}" for i in range(5)])
        air_df["target"] = air_y

        # 3. Forest Covertype Stream
        cover_X = np.random.randn(1000, 6)
        cover_y = (cover_X[:, 0] + cover_X[:, 4] > 0.5).astype(int)
        cover_df = pd.DataFrame(cover_X, columns=[f"feature_{i}" for i in range(6)])
        cover_df["target"] = cover_y

        self.datasets["Electricity (Elec2)"] = elec_df
        self.datasets["Airlines Delay"] = air_df
        self.datasets["Forest Covertype"] = cover_df
        
        self.set_active_dataset("Electricity (Elec2)")

    def set_active_dataset(self, dataset_name: str):
        if dataset_name not in self.datasets:
            raise ValueError(f"Dataset {dataset_name} not found.")
        self.active_dataset_name = dataset_name
        self.current_index = 0

    def add_custom_csv(self, name: str, df: pd.DataFrame, target_column: str = "target"):
        # Auto-detect target column if specified column isn't found
        if target_column not in df.columns:
            target_column = df.columns[-1]

        X = df.drop(columns=[target_column])
        y = df[target_column]

        # One-hot encode categorical features
        X = pd.get_dummies(X, drop_first=True)
        
        # Encode non-numeric targets into standard integers
        if y.dtype == 'object' or str(y.dtype).startswith('category'):
            y = self.label_encoder.fit_transform(y)

        # Fill any missing values with 0
        X = X.fillna(0)

        # Scale features and convert explicitly to clean DataFrames
        scaled_X = self.scaler.fit_transform(X)
        clean_df = pd.DataFrame(scaled_X, columns=X.columns)
        clean_df["target"] = np.array(y).astype(int)

        self.datasets[name] = clean_df
        self.set_active_dataset(name)

    def get_next_sample(self):
        df = self.datasets[self.active_dataset_name]
        if self.current_index >= len(df):
            self.current_index = 0

        row = df.iloc[self.current_index]
        self.current_index += 1

        # Cast all feature values to native Python floats for clean JSON serialization
        features = [float(x) for x in row.drop("target").to_numpy()]
        ground_truth = int(row["target"])

        return features, ground_truth

    def list_datasets(self):
        return list(self.datasets.keys())