import React, { useState } from 'react';
import { Cpu, CheckCircle2, XCircle, Download, FileCode, Hash, Clock, Award } from 'lucide-react';

export default function ArbiterProofViewer({ z3ProofCertificate, jsonldProof }) {
  const [activeTab, setActiveTab] = useState('smtlib');

  if (!z3ProofCertificate) {
    return (
      <div className="glass-panel" style={{ padding: '30px', textAlign: 'center' }}>
        <Cpu size={36} style={{ color: 'var(--text-dim)', marginBottom: '10px' }} />
        <h3 style={{ fontSize: '0.95rem', color: 'var(--text-muted)' }}>ARBITER Z3 Verification Idle</h3>
        <p style={{ fontSize: '0.78rem', color: 'var(--text-dim)', marginTop: '4px' }}>
          Execute an adversarial rollout to generate formal SMT-LIB2 logic formulas and prove mathematical causality.
        </p>
      </div>
    );
  }

  const handleDownloadJSONLD = () => {
    if (!jsonldProof) return;
    const blob = new Blob([JSON.stringify(jsonldProof, null, 2)], { type: 'application/ld+json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${z3ProofCertificate.certificate_id}.jsonld`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="glass-panel" style={{ padding: '20px' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Cpu size={18} style={{ color: 'var(--accent-cyan)' }} />
          <h3 style={{ fontSize: '0.95rem', fontWeight: '700' }}>
            ARBITER Formal Z3 SMT Verification & Proof Certificate
          </h3>
          <span className="badge badge-purple">MICROSOFT Z3 4.12+</span>
        </div>

        {/* Proven Badge */}
        {z3ProofCertificate.is_provably_causal ? (
          <span className="badge badge-emerald" style={{ padding: '4px 10px', fontSize: '0.75rem' }}>
            <CheckCircle2 size={13} /> FORMALLY PROVEN: $B \implies D$ (UNSAT)
          </span>
        ) : (
          <span className="badge badge-crimson" style={{ padding: '4px 10px', fontSize: '0.75rem' }}>
            <XCircle size={13} /> INCONCLUSIVE / INDEPENDENT
          </span>
        )}
      </div>

      {/* Proof Metrics Strip */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
        gap: '10px',
        marginBottom: '14px',
        background: 'rgba(5, 8, 14, 0.7)',
        padding: '10px 14px',
        borderRadius: '8px',
        border: '1px solid rgba(255, 255, 255, 0.05)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Clock size={14} style={{ color: 'var(--accent-cyan)' }} />
          <div>
            <div style={{ fontSize: '0.68rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>SOLVER LATENCY</div>
            <div style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--accent-cyan)' }}>
              {z3ProofCertificate.solver_execution_time_ms} ms
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Award size={14} style={{ color: 'var(--accent-emerald)' }} />
          <div>
            <div style={{ fontSize: '0.68rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>PROOF DEPTH</div>
            <div style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--accent-emerald)' }}>
              {z3ProofCertificate.proof_tree_depth} Proof Steps
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Hash size={14} style={{ color: 'var(--accent-purple)' }} />
          <div>
            <div style={{ fontSize: '0.68rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>SMT VARIABLES</div>
            <div style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--accent-purple)' }}>
              {z3ProofCertificate.smt_formula.variables.length} Boolean Predicates
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end' }}>
          <button
            onClick={handleDownloadJSONLD}
            className="btn btn-outline"
            style={{ fontSize: '0.75rem', padding: '5px 10px', color: 'var(--accent-cyan)' }}
          >
            <Download size={13} /> Export JSON-LD
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '10px' }}>
        <button
          onClick={() => setActiveTab('smtlib')}
          style={{
            background: activeTab === 'smtlib' ? 'rgba(0, 242, 254, 0.15)' : 'transparent',
            color: activeTab === 'smtlib' ? 'var(--accent-cyan)' : 'var(--text-muted)',
            border: 'none',
            padding: '4px 10px',
            borderRadius: '6px',
            fontSize: '0.78rem',
            fontFamily: 'var(--font-mono)',
            cursor: 'pointer'
          }}
        >
          <FileCode size={13} style={{ display: 'inline', marginRight: '4px' }} /> SMT-LIB v2 Formula
        </button>

        <button
          onClick={() => setActiveTab('jsonld')}
          style={{
            background: activeTab === 'jsonld' ? 'rgba(0, 242, 254, 0.15)' : 'transparent',
            color: activeTab === 'jsonld' ? 'var(--accent-cyan)' : 'var(--text-muted)',
            border: 'none',
            padding: '4px 10px',
            borderRadius: '6px',
            fontSize: '0.78rem',
            fontFamily: 'var(--font-mono)',
            cursor: 'pointer'
          }}
        >
          <Hash size={13} style={{ display: 'inline', marginRight: '4px' }} /> JSON-LD Certificate & SHA-256
        </button>
      </div>

      {/* Code Viewer */}
      <div style={{
        background: '#04070d',
        padding: '12px 14px',
        borderRadius: '8px',
        border: '1px solid rgba(255, 255, 255, 0.06)',
        maxHeight: '220px',
        overflowY: 'auto',
        fontFamily: 'var(--font-mono)',
        fontSize: '0.76rem',
        color: '#e2e8f0',
        lineHeight: '1.5'
      }}>
        {activeTab === 'smtlib' ? (
          <pre style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
            {z3ProofCertificate.smt_formula.smtlib_code}
          </pre>
        ) : (
          <pre style={{ margin: 0, whiteSpace: 'pre-wrap', color: '#38bdf8' }}>
            {JSON.stringify(jsonldProof, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}
