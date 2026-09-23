import React from 'react';
import { Shield, Cpu, Activity, Award, Sparkles, Terminal, FileText, BarChart3, GitBranch } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, onOpenReport, systemOnline }) {
  return (
    <header style={{
      borderBottom: '1px solid var(--border-color)',
      background: 'rgba(7, 9, 14, 0.85)',
      backdropFilter: 'blur(20px)',
      position: 'sticky',
      top: 0,
      zIndex: 50,
      padding: '12px 24px'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', maxWidth: '1600px', margin: '0 auto' }}>
        {/* Logo & Title */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, rgba(255, 51, 102, 0.2) 0%, rgba(0, 242, 254, 0.2) 100%)',
            border: '1px solid rgba(0, 242, 254, 0.3)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.3rem'
          }}>
            💀
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <h1 style={{ fontSize: '1.25rem', fontWeight: '800', letterSpacing: '-0.02em', background: 'linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                THANATOS
              </h1>
              <span className="badge badge-crimson">RESEARCH PLATFORM</span>
              <span className="badge badge-cyan">Z3 SMT SOLVER</span>
            </div>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
              Temporal Hallucination & Neurosymbolic Attack Engine • VIT Pune | TY CS D-16
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(13, 18, 29, 0.8)', padding: '4px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
          <button
            onClick={() => setActiveTab('studio')}
            className={`btn ${activeTab === 'studio' ? 'btn-primary' : 'btn-outline'}`}
            style={{ padding: '8px 14px', fontSize: '0.82rem', fontWeight: '600' }}
          >
            <Activity size={15} /> 1. Simulator
          </button>
          <button
            onClick={() => setActiveTab('dag')}
            className={`btn ${activeTab === 'dag' ? 'btn-primary' : 'btn-outline'}`}
            style={{ padding: '8px 14px', fontSize: '0.82rem', fontWeight: '600' }}
          >
            <GitBranch size={15} /> 2. Belief Graph
          </button>
          <button
            onClick={() => setActiveTab('proof')}
            className={`btn ${activeTab === 'proof' ? 'btn-primary' : 'btn-outline'}`}
            style={{ padding: '8px 14px', fontSize: '0.82rem', fontWeight: '600' }}
          >
            <Cpu size={15} /> 3. Z3 Math Proof
          </button>
          <button
            onClick={() => setActiveTab('defense')}
            className={`btn ${activeTab === 'defense' ? 'btn-primary' : 'btn-outline'}`}
            style={{ padding: '8px 14px', fontSize: '0.82rem', fontWeight: '600' }}
          >
            <Shield size={15} /> 4. Security Radar
          </button>
          <button
            onClick={() => setActiveTab('benchmarks')}
            className={`btn ${activeTab === 'benchmarks' ? 'btn-primary' : 'btn-outline'}`}
            style={{ padding: '8px 14px', fontSize: '0.82rem', fontWeight: '600' }}
          >
            <BarChart3 size={15} /> 5. Benchmarks
          </button>
        </nav>

        {/* Actions & Health Status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '6px 12px', borderRadius: '20px', background: systemOnline ? 'rgba(6, 214, 160, 0.08)' : 'rgba(255, 51, 102, 0.08)', border: `1px solid ${systemOnline ? 'rgba(6, 214, 160, 0.25)' : 'rgba(255, 51, 102, 0.25)'}` }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: systemOnline ? 'var(--accent-emerald)' : 'var(--accent-crimson)', boxShadow: systemOnline ? '0 0 8px var(--accent-emerald)' : '0 0 8px var(--accent-crimson)' }} />
            <span style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', fontWeight: '600', color: systemOnline ? 'var(--accent-emerald)' : 'var(--accent-crimson)' }}>
              {systemOnline ? 'SYSTEM READY' : 'OFFLINE'}
            </span>
          </div>

          <button
            onClick={onOpenReport}
            className="btn btn-outline"
            style={{ borderColor: 'rgba(0, 242, 254, 0.4)', color: 'var(--accent-cyan)', fontSize: '0.8rem' }}
          >
            <FileText size={15} /> Export Audit Report
          </button>
        </div>
      </div>
    </header>
  );
}
