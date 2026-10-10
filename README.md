# RetrainWise: Lifecycle-Aware Agentic Decision Engine for ML Retraining

RetrainWise is an autonomous, agentic system designed to evaluate real-time model staleness, concept drift, and performance degradation to determine the economic viability of ML model retraining in production.

## Features

**Agentic Orchestration Layer** : Autonomous LLM/rule-hybrid planner (`l3_agent.py`) that queries monitoring dashboards and cost metrics to produce explainable recommendations.

**Drift Simulation Harness** : Controlled simulation module (`simulation.py`) that injects sudden, gradual, or seasonal drift points and varying cost regimes.

**Empirical Evaluation & Comparative Analysis** : Benchmarking module (`evaluation.py`) that compares the RetrainWise policy against standard baselines (Calendar-based, Drift-trigger only, and CARA).

**Human-Readable Explainability Reports** : Frontend component (`DecisionReport.jsx`) rendering natural-language justifications and step-by-step reasoning chains.

**Multi-Dataset Support** : Pre-loaded with standard streaming benchmarks and supports custom CSV file uploads with automated preprocessing.

**Live Visual Analytics** : Real-time stream telemetry visualization using React, Tailwind CSS, and Recharts.

**INR Cost-Benefit Engine** : Evaluates expected accuracy recovery benefits vs. compute, engineering, and deployment costs in Indian Rupees (₹).

## Architecture
**Backend:** FastAPI, scikit-learn, pandas, NumPy, custom simulation & evaluation harnesses, agentic planner.
**Frontend:** React, Vite, Tailwind CSS, Recharts, Lucide Icons, Explainability Decision Report UI.

---

## Quickstart

### Backend Setup

cd backend
python -m venv venv

# Activate virtual environment (Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
uvicorn app:app --reload --port 8000

### Frontend Setup
cd frontend
npm install
npm run dev