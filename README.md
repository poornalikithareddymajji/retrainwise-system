# RetrainWise: Lifecycle-Aware Agentic Decision Engine for ML Retraining

RetrainWise is an autonomous, agentic system designed to evaluate real-time model staleness, concept drift, and performance degradation to determine the economic viability of ML model retraining in production.

## Features
- **INR Cost-Benefit Engine:** Evaluates expected accuracy recovery benefits vs. compute, engineering, and deployment costs in Indian Rupees (₹).
- **Multi-Dataset Support:** Pre-loaded with standard benchmarks (Electricity, Airlines, Forest Covertype) and supports custom CSV file uploads.
- **Automated Data Preprocessing:** Includes categorical one-hot encoding, missing value imputation, and automated feature scaling.
- **Live Visual Analytics:** Real-time stream telemetry visualization using React, Tailwind CSS, and Recharts.

## Architecture
- **Backend:** FastAPI, scikit-learn, pandas, NumPy
- **Frontend:** React, Vite, Tailwind CSS, Recharts, Lucide Icons

## Quickstart

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000