from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import io

from src.l1_monitoring import DriftAndStalenessMonitor
from src.l2_decision import CostBenefitDecisionEngine
from src.l3_agent import AgenticOrchestrator
from src.l4_action import ActionExecutor
from data.dataset_manager import StreamDatasetManager

app = FastAPI(title="RetrainWise Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

monitor = DriftAndStalenessMonitor()
engine = CostBenefitDecisionEngine()
agent = AgenticOrchestrator(engine)
executor = ActionExecutor()
data_manager = StreamDatasetManager()

@app.get("/health")
def health():
    return {"status": "online", "system": "RetrainWise Agent System"}

@app.get("/api/datasets")
def get_datasets():
    return {
        "active_dataset": data_manager.active_dataset_name,
        "available_datasets": data_manager.list_datasets()
    }

@app.post("/api/select-dataset")
def select_dataset(payload: dict):
    dataset_name = payload.get("dataset_name")
    data_manager.set_active_dataset(dataset_name)
    monitor.reset()
    executor.reset()  # Reset model weights for new dataset feature shapes
    return {"status": "success", "active_dataset": dataset_name}

@app.post("/api/upload-csv")
async def upload_csv(file: UploadFile = File(...), target_col: str = Form("target")):
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    dataset_name = file.filename.replace(".csv", "")
    
    data_manager.add_custom_csv(dataset_name, df, target_column=target_col)
    monitor.reset()
    executor.reset()  # Reset model weights for custom CSV feature shapes
    return {"status": "success", "active_dataset": dataset_name}

@app.post("/api/step-stream")
def step_stream():
    features, ground_truth = data_manager.get_next_sample()
    
    # Reshape features to 2D array (1, n_features)
    x_input = np.array(features).reshape(1, -1)
    
    y_pred = executor.predict(x_input)
    telemetry = monitor.update(ground_truth, y_pred)
    agent_output = agent.run_agent_loop(telemetry)

    if agent_output["decision"]["recommended_action"] == "RETRAIN_NOW":
        executor.train_or_update(x_input, np.array([ground_truth]))
        monitor.reset()

    return {
        "dataset_name": data_manager.active_dataset_name,
        "prediction": y_pred,
        "ground_truth": ground_truth,
        "agent_response": agent_output
    }