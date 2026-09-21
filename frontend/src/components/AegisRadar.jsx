import React, { useState, useEffect } from 'react';
import { ShieldAlert, ShieldCheck, AlertTriangle, Shield, CheckCircle2, Lock, ExternalLink } from 'lucide-react';

export default function AegisRadar({ defenseReport }) {
  const [complianceMatrix, setComplianceMatrix] = useState(null);

  useEffect(() => {
    fetch('/api/defense/compliance-matrix')
      .then(res => res.json())
      .then(data => setComplianceMatrix(data))
      .catch(err => console.error("Failed to load compliance matrix", err));
  }, []);

  const integrity = defenseReport ? defenseReport.system_integrity_score : 1.0;
  const alerts = defenseReport ? defenseReport.alerts_triggered : [];
  const recommendations = defenseReport ? defenseReport.mitigation_recommendations : [
    "Continuous neurosymbolic belief consistency monitoring active.",
    "Temporal paradox detection enabled."
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {/* Top Row: System Integrity & Alert Stream */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '16px' }}>
        {/* Integrity Gauge Card */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Shield size={18} style={{ color: 'var(--accent-cyan)' }} />
              <h3 style={{ fontSize: '0.95rem', fontWeight: '700' }}>AEGIS System Integrity Score</h3>
            </div>
            <span className={`badge ${integrity > 0.7 ? 'badge-emerald' : 'badge-crimson'}`}>
              {integrity > 0.7 ? 'SECURE' : 'COMPROMISED'}
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '20px', margin: '20px 0' }}>
            <div style={{
              width: '100px',
              height: '100px',
              borderRadius: '50%',
              border: `6px solid ${integrity > 0.7 ? 'var(--accent-emerald)' : 'var(--accent-crimson)'}`,
              boxShadow: integrity > 0.7 ? 'var(--glow-emerald)' : 'var(--glow-crimson)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              background: 'rgba(5, 8, 14, 0.8)'
            }}>
              <span style={{ fontSize: '1.4rem', fontWeight: '800', fontFamily: 'var(--font-mono)' }}>
                {(integrity * 100).toFixed(0)}%
              </span>
              <span style={{ fontSize: '0.65rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>
                TRUST INDEX
              </span>
            </div>

            <div style={{ flexGrow: 1 }}>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-main)', lineHeight: '1.4' }}>
                {integrity > 0.7
                  ? "All inter-agent handoffs exhibit nominal semantic coherence with zero unverified belief state drifts."
                  : "Critical belief state drift detected! Catastrophic false premise propagated through downstream agent handoffs."}
              </p>
              <div style={{ display: 'flex', gap: '8px', marginTop: '10px' }}>
                <span className="badge badge-purple">{alerts.length} ALERTS FLAGGED</span>
                <span className="badge badge-cyan">PARADOX CHECK: ACTIVE</span>
              </div>
            </div>
          </div>

          {/* Recommendations */}
          <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '12px' }}>
            <div style={{ fontSize: '0.72rem', color: 'var(--accent-cyan)', fontFamily: 'var(--font-mono)', marginBottom: '6px' }}>
              AEGIS REMEDIATION ACTIONS:
            </div>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {recommendations.map((rec, idx) => (
                <li key={idx} style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'flex', alignItems: 'flex-start', gap: '6px' }}>
                  <CheckCircle2 size={12} style={{ color: 'var(--accent-emerald)', marginTop: '2px', flexShrink: 0 }} />
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Real-Time Anomaly Alerts Feed */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <ShieldAlert size={18} style={{ color: 'var(--accent-crimson)' }} />
              <h3 style={{ fontSize: '0.95rem', fontWeight: '700' }}>Real-Time Anomaly Radar</h3>
            </div>
            <span className="badge badge-crimson">{alerts.length} THREATS</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '280px', overflowY: 'auto' }}>
            {alerts.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '30px', color: 'var(--text-dim)' }}>
                <ShieldCheck size={32} style={{ margin: '0 auto 8px', color: 'var(--accent-emerald)' }} />
                <p style={{ fontSize: '0.8rem' }}>No active belief anomalies detected in pipeline state.</p>
              </div>
            ) : (
              alerts.map(alert => (
                <div
                  key={alert.alert_id}
                  style={{
                    background: 'rgba(30, 8, 16, 0.7)',
                    border: '1px solid rgba(255, 51, 102, 0.3)',
                    borderRadius: '8px',
                    padding: '10px 12px'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <span className="badge badge-crimson" style={{ fontSize: '0.65rem' }}>{alert.severity}</span>
                      <span style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--accent-cyan)' }}>
                        [{alert.source_agent}]
                      </span>
                    </div>
                    <span style={{ fontSize: '0.72rem', fontFamily: 'var(--font-mono)', color: 'var(--accent-crimson)' }}>
                      Divergence: {(alert.anomaly_score * 100).toFixed(0)}%
                    </span>
                  </div>

                  <p style={{ fontSize: '0.78rem', color: '#f8fafc', marginBottom: '4px' }}>
                    "{alert.flagged_proposition}"
                  </p>

                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                    {alert.owasp_mapping?.map((o, i) => (
                      <span key={i} className="badge badge-amber" style={{ fontSize: '0.62rem' }}>{o}</span>
                    ))}
                    {alert.mitre_mapping?.map((m, i) => (
                      <span key={i} className="badge badge-purple" style={{ fontSize: '0.62rem' }}>{m}</span>
                    ))}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Bottom Section: OWASP Top 10 for LLM & MITRE ATLAS Matrix */}
      {complianceMatrix && (
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
            <Lock size={18} style={{ color: 'var(--accent-purple)' }} />
            <h3 style={{ fontSize: '0.95rem', fontWeight: '700' }}>
              OWASP Top 10 for LLMs & MITRE ATLAS Adversarial Mapping
            </h3>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '12px' }}>
            {/* OWASP List */}
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--accent-amber)', fontFamily: 'var(--font-mono)', marginBottom: '8px' }}>
                OWASP TOP 10 FOR LLM VULNERABILITIES COVERED:
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {complianceMatrix.owasp_top_10?.map((item, i) => (
                  <div key={i} style={{ background: 'rgba(13, 18, 29, 0.8)', padding: '8px 10px', borderRadius: '6px', border: '1px solid rgba(255, 255, 255, 0.04)' }}>
                    <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--accent-amber)' }}>{item.id}</div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>{item.description}</div>
                    <div style={{ fontSize: '0.68rem', color: 'var(--accent-cyan)', fontFamily: 'var(--font-mono)', marginTop: '2px' }}>
                      ⚡ THANATOS Defense: {item.thanatos_coverage}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* MITRE ATLAS List */}
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--accent-purple)', fontFamily: 'var(--font-mono)', marginBottom: '8px' }}>
                MITRE ATLAS ADVERSARIAL AI TACTICS TESTED:
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {complianceMatrix.mitre_atlas_tactics?.map((item, i) => (
                  <div key={i} style={{ background: 'rgba(13, 18, 29, 0.8)', padding: '8px 10px', borderRadius: '6px', border: '1px solid rgba(255, 255, 255, 0.04)' }}>
                    <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--accent-purple)' }}>{item.id}</div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>{item.description}</div>
                    <div style={{ fontSize: '0.68rem', color: 'var(--accent-crimson)', fontFamily: 'var(--font-mono)', marginTop: '2px' }}>
                      💀 Attack Module: {item.thanatos_module}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
