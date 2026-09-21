import React, { useState } from 'react';
import { BarChart3, Play, Activity, Clock, Zap, Shield, Target } from 'lucide-react';

export default function BenchmarkView() {
  const [benchmarkResult, setBenchmarkResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [trials, setTrials] = useState(3);
  const [scenario, setScenario] = useState('devops_pipeline');

  const handleRunBenchmarks = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/benchmark/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pipeline_name: scenario,
          trials_per_vector: trials
        })
      });
      const data = await res.json();
      setBenchmarkResult(data);
    } catch (err) {
      console.error("Benchmark failed", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {/* Benchmark Control Card */}
      <div className="glass-panel" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <BarChart3 size={18} style={{ color: 'var(--accent-cyan)' }} />
            <h3 style={{ fontSize: '0.95rem', fontWeight: '700' }}>
              Automated Neurosymbolic Empirical Benchmark Suite
            </h3>
            <span className="badge badge-purple">SHADE-ARENA PROTOCOL</span>
          </div>

          <button
            onClick={handleRunBenchmarks}
            disabled={loading}
            className="btn btn-primary"
            style={{ padding: '8px 16px' }}
          >
            <Play size={15} /> {loading ? 'Running Trials...' : 'Run Quantitative Benchmark'}
          </button>
        </div>

        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', marginBottom: '4px' }}>
              TARGET PIPELINE
            </label>
            <select
              value={scenario}
              onChange={(e) => setScenario(e.target.value)}
              style={{
                padding: '6px 12px',
                borderRadius: '6px',
                background: 'rgba(13, 18, 29, 0.9)',
                border: '1px solid var(--border-color)',
                color: 'var(--text-main)',
                fontSize: '0.8rem',
                outline: 'none'
              }}
            >
              <option value="devops_pipeline">DevOps CI/CD Deployment Swarm</option>
              <option value="financial_research">Financial & Legal Risk Swarm</option>
              <option value="healthcare_rag">Clinical Diagnostic RAG System</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', marginBottom: '4px' }}>
              TRIALS PER VECTOR
            </label>
            <select
              value={trials}
              onChange={(e) => setTrials(Number(e.target.value))}
              style={{
                padding: '6px 12px',
                borderRadius: '6px',
                background: 'rgba(13, 18, 29, 0.9)',
                border: '1px solid var(--border-color)',
                color: 'var(--text-main)',
                fontSize: '0.8rem',
                outline: 'none'
              }}
            >
              <option value={2}>2 Trials (Rapid)</option>
              <option value={3}>3 Trials (Standard)</option>
              <option value={5}>5 Trials (Deep Empirical)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Benchmark Results */}
      {benchmarkResult ? (
        <div className="glass-panel" style={{ padding: '20px' }}>
          {/* Summary Metric Header */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '12px',
            marginBottom: '20px',
            background: 'rgba(5, 8, 14, 0.7)',
            padding: '14px',
            borderRadius: '8px'
          }}>
            <div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>OVERALL ATTACK SUCCESS RATE</div>
              <div style={{ fontSize: '1.4rem', fontWeight: '800', color: 'var(--accent-crimson)' }}>
                {(benchmarkResult.overall_asr * 100).toFixed(1)}%
              </div>
            </div>

            <div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>MEAN CASCADE DEPTH</div>
              <div style={{ fontSize: '1.4rem', fontWeight: '800', color: 'var(--accent-amber)' }}>
                {benchmarkResult.mean_cascade_depth} Handoffs
              </div>
            </div>

            <div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>TOTAL EVALUATION DURATION</div>
              <div style={{ fontSize: '1.4rem', fontWeight: '800', color: 'var(--accent-cyan)' }}>
                {benchmarkResult.total_duration_sec}s
              </div>
            </div>

            <div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>TOTAL ROLLOUT TRIALS</div>
              <div style={{ fontSize: '1.4rem', fontWeight: '800', color: 'var(--accent-purple)' }}>
                {benchmarkResult.total_rollouts} Runs
              </div>
            </div>
          </div>

          {/* Per-Vector Breakdown Table */}
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.8rem', fontFamily: 'var(--font-mono)' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)', textAlign: 'left' }}>
                  <th style={{ padding: '10px' }}>INJECTION VECTOR</th>
                  <th style={{ padding: '10px' }}>TRIALS</th>
                  <th style={{ padding: '10px' }}>ASR (SUCCESS)</th>
                  <th style={{ padding: '10px' }}>AVG CASCADE DEPTH</th>
                  <th style={{ padding: '10px' }}>Z3 SOLVER TIME</th>
                  <th style={{ padding: '10px' }}>AEGIS EVASION RATE</th>
                </tr>
              </thead>
              <tbody>
                {benchmarkResult.vector_results?.map((v, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.04)' }}>
                    <td style={{ padding: '10px', color: 'var(--text-main)', fontWeight: '600' }}>
                      {v.vector_name.toUpperCase()}
                    </td>
                    <td style={{ padding: '10px', color: 'var(--text-muted)' }}>{v.trials}</td>
                    <td style={{ padding: '10px' }}>
                      <span className="badge badge-crimson">{(v.attack_success_rate * 100).toFixed(0)}%</span>
                    </td>
                    <td style={{ padding: '10px', color: 'var(--accent-amber)' }}>{v.mean_cascade_depth} steps</td>
                    <td style={{ padding: '10px', color: 'var(--accent-cyan)' }}>{v.mean_z3_verification_time_ms} ms</td>
                    <td style={{ padding: '10px' }}>
                      <span className="badge badge-purple">{(v.aegis_evasion_rate * 100).toFixed(0)}%</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="glass-panel" style={{ padding: '40px', textAlign: 'center' }}>
          <Activity size={36} style={{ color: 'var(--text-dim)', margin: '0 auto 10px' }} />
          <h3 style={{ fontSize: '0.95rem', color: 'var(--text-muted)' }}>No Active Benchmark Rollout</h3>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-dim)', marginTop: '4px' }}>
            Click "Run Quantitative Benchmark" to evaluate ASR and Z3 verification latency across all 5 vectors.
          </p>
        </div>
      )}
    </div>
  );
}
