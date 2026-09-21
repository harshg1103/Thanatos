import React, { useState } from 'react';
import { Terminal, Shield, AlertCircle, CheckCircle, ChevronDown, ChevronRight, User, Cpu } from 'lucide-react';

export default function AgentTerminal({ turns, finalOutput, isCorrupted }) {
  const [expandedTurns, setExpandedTurns] = useState({});

  if (!turns || turns.length === 0) {
    return (
      <div className="glass-panel" style={{ padding: '30px', textAlign: 'center' }}>
        <Terminal size={36} style={{ color: 'var(--text-dim)', marginBottom: '10px' }} />
        <h3 style={{ fontSize: '0.95rem', color: 'var(--text-muted)' }}>Live Agent Terminal Standby</h3>
        <p style={{ fontSize: '0.78rem', color: 'var(--text-dim)', marginTop: '4px' }}>
          Autonomous agent scratchpad thoughts and inter-agent handoff logs will stream here during execution.
        </p>
      </div>
    );
  }

  const toggleTurn = (idx) => {
    setExpandedTurns(prev => ({
      ...prev,
      [idx]: !prev[idx]
    }));
  };

  return (
    <div className="glass-panel" style={{ padding: '20px' }}>
      {/* Terminal Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Terminal size={18} style={{ color: 'var(--accent-emerald)' }} />
          <h3 style={{ fontSize: '0.95rem', fontWeight: '700' }}>
            Multi-Agent Autonomous Execution Scratchpad
          </h3>
          <span className="badge badge-emerald">{turns.length} HANDOFFS</span>
        </div>

        {isCorrupted ? (
          <span className="badge badge-crimson">
            <AlertCircle size={12} /> CASCADE PROPAGATED
          </span>
        ) : (
          <span className="badge badge-emerald">
            <CheckCircle size={12} /> NOMINAL EXECUTION
          </span>
        )}
      </div>

      {/* Turn by Turn Agent Cards */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {turns.map((turn, idx) => {
          const isExpanded = expandedTurns[idx] !== false; // expanded by default
          const isTurnCorrupted = turn.is_corrupted;

          return (
            <div
              key={idx}
              style={{
                background: isTurnCorrupted ? 'rgba(30, 10, 18, 0.7)' : 'rgba(10, 16, 26, 0.7)',
                border: `1px solid ${isTurnCorrupted ? 'rgba(255, 51, 102, 0.35)' : 'rgba(255, 255, 255, 0.06)'}`,
                borderRadius: '8px',
                overflow: 'hidden'
              }}
            >
              {/* Card Title Row */}
              <div
                onClick={() => toggleTurn(idx)}
                style={{
                  padding: '10px 14px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  cursor: 'pointer',
                  background: isTurnCorrupted ? 'rgba(255, 51, 102, 0.08)' : 'rgba(255, 255, 255, 0.02)',
                  borderBottom: isExpanded ? '1px solid rgba(255, 255, 255, 0.05)' : 'none'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                  <span className="badge badge-purple" style={{ fontSize: '0.7rem' }}>
                    STEP {turn.step}
                  </span>
                  <span style={{ fontSize: '0.85rem', fontWeight: '700', color: isTurnCorrupted ? '#ff8099' : 'var(--text-main)' }}>
                    [{turn.agent}] {turn.role || turn.agent}
                  </span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  {turn.injected && (
                    <span className="badge badge-crimson" style={{ fontSize: '0.68rem' }}>
                      INJECTION TRIGGER
                    </span>
                  )}
                  {isTurnCorrupted && (
                    <span className="badge badge-crimson" style={{ fontSize: '0.68rem' }}>
                      BELIEF ECHO
                    </span>
                  )}
                </div>
              </div>

              {/* Card Body */}
              {isExpanded && (
                <div style={{ padding: '12px 14px' }}>
                  {/* Scratchpad reasoning */}
                  {turn.scratchpad && (
                    <div style={{ marginBottom: '10px' }}>
                      <div style={{ fontSize: '0.7rem', color: 'var(--accent-cyan)', fontFamily: 'var(--font-mono)', marginBottom: '4px' }}>
                        INTERNAL SCRATCHPAD REASONING:
                      </div>
                      <div style={{
                        fontSize: '0.78rem',
                        fontFamily: 'var(--font-mono)',
                        color: 'var(--text-muted)',
                        background: 'rgba(5, 8, 14, 0.8)',
                        padding: '8px 10px',
                        borderRadius: '6px',
                        borderLeft: '2px solid var(--accent-cyan)'
                      }}>
                        {turn.scratchpad}
                      </div>
                    </div>
                  )}

                  {/* Output generation */}
                  <div>
                    <div style={{ fontSize: '0.7rem', color: isTurnCorrupted ? '#ff8099' : 'var(--accent-emerald)', fontFamily: 'var(--font-mono)', marginBottom: '4px' }}>
                      AGENT HANDOFF OUTPUT:
                    </div>
                    <pre style={{
                      fontSize: '0.8rem',
                      fontFamily: 'var(--font-mono)',
                      color: '#e2e8f0',
                      whiteSpace: 'pre-wrap',
                      background: '#04070d',
                      padding: '10px 12px',
                      borderRadius: '6px',
                      lineHeight: '1.45',
                      border: isTurnCorrupted ? '1px solid rgba(255, 51, 102, 0.2)' : '1px solid rgba(255, 255, 255, 0.04)'
                    }}>
                      {turn.output}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Final Autonomous Decision Box */}
      {finalOutput && (
        <div style={{
          marginTop: '16px',
          padding: '14px',
          borderRadius: '8px',
          background: isCorrupted ? 'rgba(40, 10, 20, 0.8)' : 'rgba(8, 26, 20, 0.8)',
          border: `1px solid ${isCorrupted ? 'var(--accent-crimson)' : 'var(--accent-emerald)'}`
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
            <span style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', fontWeight: '700', color: isCorrupted ? 'var(--accent-crimson)' : 'var(--accent-emerald)' }}>
              FINAL AUTONOMOUS PIPELINE DECISION
            </span>
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-main)', lineHeight: '1.4' }}>
            {finalOutput}
          </p>
        </div>
      )}
    </div>
  );
}
