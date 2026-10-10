// frontend/src/components/DecisionReport.jsx
import React from 'react';

export default function DecisionReport({ report }) {
  if (!report) return null;

  const action = report.decision?.recommended_action || report.action;
  const isRetrain = action === "RETRAIN_NOW" || action === "RETRAIN";

  return (
    <div style={{
      border: `2px solid ${isRetrain ? '#ef4444' : '#10b981'}`,
      borderRadius: '8px',
      padding: '20px',
      marginTop: '20px',
      backgroundColor: '#f9fafb',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ margin: 0, color: '#1f2937' }}>Agentic Decision Report</h3>
        <span style={{
          backgroundColor: isRetrain ? '#fee2e2' : '#d1fae5',
          color: isRetrain ? '#991b1b' : '#065f46',
          padding: '6px 12px',
          borderRadius: '20px',
          fontWeight: 'bold',
          fontSize: '14px'
        }}>
          Action: {action}
        </span>
      </div>

      <p style={{ marginTop: '12px', fontSize: '15px', color: '#374151', lineHeight: '1.5' }}>
        <strong>Natural Language Explanation:</strong> {report.explanation || "System is operating under nominal drift and cost-benefit thresholds."}
      </p>

      {report.reasoning_steps && (
        <>
          <h4 style={{ marginBottom: '8px', color: '#1f2937' }}>Agent Reasoning Chain:</h4>
          <ul style={{ paddingLeft: '20px', color: '#4b5563', margin: 0 }}>
            {report.reasoning_steps.map((step, idx) => (
              <li key={idx} style={{ marginBottom: '4px' }}>{step}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}