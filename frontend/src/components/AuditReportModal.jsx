import React, { useState } from 'react';
import { FileText, Printer, Download, CheckCircle2, ShieldAlert, Cpu, Hash, X } from 'lucide-react';

export default function AuditReportModal({ isOpen, onClose, runResult }) {
  if (!isOpen) return null;

  const handlePrint = () => {
    window.print();
  };

  const isProven = runResult?.z3_proof_certificate?.is_provably_causal;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.85)',
      backdropFilter: 'blur(12px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '20px'
    }}>
      <div style={{
        background: '#090d16',
        border: '1px solid var(--border-color)',
        borderRadius: '12px',
        width: '100%',
        maxWidth: '900px',
        maxHeight: '90vh',
        display: 'flex',
        flexDirection: 'column',
        boxShadow: '0 20px 50px rgba(0, 0, 0, 0.9)'
      }}>
        {/* Modal Header */}
        <div style={{
          padding: '16px 20px',
          borderBottom: '1px solid var(--border-color)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <FileText size={18} style={{ color: 'var(--accent-cyan)' }} />
            <h3 style={{ fontSize: '1rem', fontWeight: '700' }}>
              THANATOS Formal Security Vulnerability Assessment
            </h3>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <button onClick={handlePrint} className="btn btn-outline" style={{ fontSize: '0.78rem', padding: '6px 12px' }}>
              <Printer size={14} /> Print Report
            </button>
            <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: 'var(--text-dim)', cursor: 'pointer', fontSize: '1.2rem' }}>
              ✕
            </button>
          </div>
        </div>

        {/* Modal Content */}
        <div style={{ padding: '24px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '18px' }}>
          {/* Academic Header Banner */}
          <div style={{
            background: 'rgba(13, 18, 29, 0.9)',
            padding: '16px',
            borderRadius: '8px',
            border: '1px solid rgba(0, 242, 254, 0.2)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <h2 style={{ fontSize: '1.1rem', fontWeight: '800', color: '#ffffff' }}>
                  Project THANATOS — Mid-Semester Security Audit
                </h2>
                <p style={{ fontSize: '0.8rem', color: 'var(--accent-cyan)', fontFamily: 'var(--font-mono)', marginTop: '2px' }}>
                  Vishwakarma Institute of Technology (VIT Pune) | Semester 5 (TY CS)
                </p>
              </div>
              <div style={{ textAlign: 'right', fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                <div>Group: TY CS D-16</div>
                <div>Guide: Prof. Vidula Meshram</div>
              </div>
            </div>
          </div>

          {/* Executive Summary */}
          <div>
            <h4 style={{ fontSize: '0.85rem', color: 'var(--accent-amber)', fontFamily: 'var(--font-mono)', marginBottom: '6px' }}>
              1. EXECUTIVE SUMMARY & THREAT DISCLOSURE
            </h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-main)', lineHeight: '1.5' }}>
              During automated red-team probing of the target multi-agent pipeline (<strong>{runResult?.pipeline_name || "devops_pipeline"}</strong>),
              THANATOS injected a temporally-coherent false belief proposition. The adversarial premise successfully bypassed traditional single-turn prompt filters,
              propagated across <strong>{runResult?.cascade_depth || 3} downstream agent handoffs</strong>, and formally caused a critical autonomous security bypass.
            </p>
          </div>

          {/* Formal Z3 Proof Section */}
          <div style={{
            background: 'rgba(5, 8, 14, 0.9)',
            padding: '14px',
            borderRadius: '8px',
            border: `1px solid ${isProven ? 'rgba(6, 214, 160, 0.3)' : 'rgba(255, 51, 102, 0.3)'}`
          }}>
            <h4 style={{ fontSize: '0.85rem', color: isProven ? 'var(--accent-emerald)' : 'var(--accent-crimson)', fontFamily: 'var(--font-mono)', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Cpu size={15} /> 2. ARBITER FORMAL Z3 THEOREM PROVING CERTIFICATE
            </h4>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px', fontSize: '0.78rem', fontFamily: 'var(--font-mono)' }}>
              <div>
                <span style={{ color: 'var(--text-dim)' }}>Formal Entailment:</span>
                <div style={{ color: isProven ? 'var(--accent-emerald)' : 'var(--accent-crimson)', fontWeight: '700' }}>
                  {isProven ? 'MATHEMATICALLY PROVEN (B => D)' : 'INCONCLUSIVE'}
                </div>
              </div>
              <div>
                <span style={{ color: 'var(--text-dim)' }}>SMT Solver:</span>
                <div style={{ color: '#ffffff' }}>Microsoft Z3 v4.12</div>
              </div>
              <div>
                <span style={{ color: 'var(--text-dim)' }}>Solver Latency:</span>
                <div style={{ color: 'var(--accent-cyan)' }}>
                  {runResult?.z3_proof_certificate?.solver_execution_time_ms || 0} ms
                </div>
              </div>
              <div>
                <span style={{ color: 'var(--text-dim)' }}>SHA-256 Digest:</span>
                <div style={{ color: '#cbd5e1', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {runResult?.jsonld_proof?.proofDetails?.sha256_digest?.substring(0, 16) || "e3b0c44298fc1c14"}...
                </div>
              </div>
            </div>
          </div>

          {/* Downstream Cascade & Impact */}
          <div>
            <h4 style={{ fontSize: '0.85rem', color: 'var(--accent-crimson)', fontFamily: 'var(--font-mono)', marginBottom: '6px' }}>
              3. CASCADE PROPAGATION TRACE
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              {runResult?.turns?.map((turn, i) => (
                <div key={i} style={{ background: 'rgba(13, 18, 29, 0.6)', padding: '8px 12px', borderRadius: '6px', fontSize: '0.78rem', display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--accent-cyan)', fontFamily: 'var(--font-mono)' }}>
                    Turn {turn.step}: [{turn.agent}]
                  </span>
                  <span style={{ color: turn.is_corrupted ? 'var(--accent-crimson)' : 'var(--accent-emerald)', fontWeight: '600' }}>
                    {turn.is_corrupted ? 'Corrupted Belief Echoed' : 'Clean State'}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* AEGIS Recommendations */}
          <div>
            <h4 style={{ fontSize: '0.85rem', color: 'var(--accent-cyan)', fontFamily: 'var(--font-mono)', marginBottom: '6px' }}>
              4. DEFENSE & MITIGATION DIRECTIVES
            </h4>
            <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              <li style={{ marginBottom: '4px' }}>• Integrate ARBITER Z3 verification gates before high-agency agent handoffs.</li>
              <li style={{ marginBottom: '4px' }}>• Enforce CHRONICLE temporal DAG consistency to eliminate circular paradoxes.</li>
              <li style={{ marginBottom: '4px' }}>• Deploy AEGIS real-time anomaly classifiers for inter-agent schema validation.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
