import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Activity, ShieldAlert, Cpu, IndianRupee, Database, Upload } from 'lucide-react';
import DecisionReport from './components/DecisionReport';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export default function App() {
  const [datasets, setDatasets] = useState([]);
  const [activeDataset, setActiveDataset] = useState('');
  const [metricsHistory, setMetricsHistory] = useState([]);
  const [latestReport, setLatestReport] = useState(null);
  const [stepCount, setStepCount] = useState(0);

  const fetchDatasets = async () => {
    try {
      const res = await fetch(`${BACKEND_URL}/api/datasets`);
      const data = await res.json();
      setDatasets(data.available_datasets || []);
      if (data.active_dataset) {
        setActiveDataset(data.active_dataset);
      }
    } catch (err) {
      console.error("Error loading datasets:", err);
    }
  };

  useEffect(() => {
    fetchDatasets();
  }, []);

  const handleSelectDataset = async (e) => {
    const selected = e.target.value;
    setActiveDataset(selected);
    try {
      await fetch(`${BACKEND_URL}/api/select-dataset`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dataset_name: selected })
      });
    } catch (err) {
      console.error("Dataset Selection Error:", err);
    }

    setMetricsHistory([]);
    setLatestReport(null);
    setStepCount(0);
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('target_col', 'target');

    try {
      await fetch(`${BACKEND_URL}/api/upload-csv`, {
        method: 'POST',
        body: formData
      });
      await fetchDatasets();
    } catch (err) {
      console.error("Upload Error:", err);
    }

    setMetricsHistory([]);
    setLatestReport(null);
    setStepCount(0);
  };

  const runSimulationStep = async () => {
    try {
      const res = await fetch(`${BACKEND_URL}/api/step-stream`, { method: 'POST' });
      const data = await res.json();
      
      if (!data || !data.agent_response) return;

      const newStep = stepCount + 1;
      setStepCount(newStep);
      setLatestReport(data.agent_response);

      const decision = data.agent_response.decision || {};
      const benefitInr = decision.expected_benefit_inr !== undefined 
        ? decision.expected_benefit_inr.toFixed(2)
        : ((decision.expected_benefit_usd || 0) * 83).toFixed(2);

      const telemetry = data.agent_response.telemetry || {};

      setMetricsHistory((prev) => [
        ...prev.slice(-29),
        {
          step: newStep,
          errorRate: ((telemetry.rolling_error_rate || 0) * 100).toFixed(1),
          staleness: (telemetry.staleness_score || 0).toFixed(2),
          benefit: benefitInr
        }
      ]);
    } catch (err) {
      console.error("Stream Error:", err);
    }
  };

  useEffect(() => {
    const timer = setInterval(() => runSimulationStep(), 1000);
    return () => clearInterval(timer);
  }, [stepCount]);

  const getBenefitDisplay = () => {
    if (!latestReport || !latestReport.decision) return '₹0.00';
    const d = latestReport.decision;
    if (d.expected_benefit_inr !== undefined) {
      return `₹${d.expected_benefit_inr.toFixed(2)}`;
    }
    return `₹${((d.expected_benefit_usd || 0) * 83).toFixed(2)}`;
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8">
      {/* Header Bar */}
      <header className="flex flex-wrap justify-between items-center border-b border-slate-800 pb-6 mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-sky-400">RetrainWise Dashboard</h1>
          <p className="text-slate-400 text-sm">Lifecycle-Aware Agent for Cost-Benefit Training Decisions</p>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 px-3 py-2 rounded-lg">
            <Database className="w-4 h-4 text-sky-400" />
            <select 
              value={activeDataset} 
              onChange={handleSelectDataset} 
              className="bg-transparent text-sm font-medium focus:outline-none cursor-pointer"
            >
              {datasets.map((ds) => (
                <option key={ds} value={ds} className="bg-slate-900 text-slate-200">
                  {ds}
                </option>
              ))}
            </select>
          </div>

          <label className="flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white px-4 py-2 rounded-lg text-sm font-medium cursor-pointer transition">
            <Upload className="w-4 h-4" /> Upload Custom CSV
            <input type="file" accept=".csv" onChange={handleFileUpload} className="hidden" />
          </label>
        </div>
      </header>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span>Rolling Error Rate</span>
            <Activity className="w-5 h-5 text-sky-400" />
          </div>
          <div className="text-2xl font-bold">
            {latestReport && latestReport.telemetry ? `${(latestReport.telemetry.rolling_error_rate * 100).toFixed(1)}%` : '0%'}
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span>Staleness Index</span>
            <Cpu className="w-5 h-5 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold">
            {latestReport && latestReport.telemetry ? latestReport.telemetry.staleness_score.toFixed(2) : '0.00'}
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span>Retrain Benefit</span>
            <IndianRupee className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400">
            {getBenefitDisplay()}
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span>Active Action</span>
            <ShieldAlert className="w-5 h-5 text-yellow-400" />
          </div>
          <div className="text-xl font-bold text-yellow-400">
            {latestReport && latestReport.decision ? latestReport.decision.recommended_action : 'INITIALIZING'}
          </div>
        </div>
      </div>

      {/* Charts & Agent Terminal */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 p-6 rounded-xl">
          <h2 className="text-lg font-semibold mb-4 text-slate-200">Stream Analytics: {activeDataset}</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={metricsHistory}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="step" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                <Line type="monotone" dataKey="errorRate" stroke="#38bdf8" strokeWidth={2} name="Error Rate (%)" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl flex flex-col justify-between">
          <div>
            <h2 className="text-lg font-semibold mb-4 text-slate-200">Agent Decision Justification</h2>
            <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 text-sm font-mono text-slate-300 leading-relaxed min-h-48 whitespace-pre-line">
              {latestReport ? latestReport.agent_justification : 'Awaiting stream telemetry...'}
            </div>
          </div>
          <div className="mt-4 pt-4 border-t border-slate-800 text-xs text-slate-500">
            Active Dataset: {activeDataset}
          </div>
        </div>
      </div>

      {/* Explainable Decision Report Component */}
      {latestReport && (
        <DecisionReport report={latestReport} />
      )}
    </div>
  );
}