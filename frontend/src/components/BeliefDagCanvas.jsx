import React, { useState } from 'react';
import { Network, AlertTriangle, CheckCircle2, ShieldAlert, Zap, Info } from 'lucide-react';

export default function BeliefDagCanvas({ beliefGraph, cascadeDepth, onSelectNode }) {
  const [selectedNodeId, setSelectedNodeId] = useState(null);

  if (!beliefGraph || !beliefGraph.nodes || beliefGraph.nodes.length === 0) {
    return (
      <div className="glass-panel" style={{ padding: '40px', textAlign: 'center' }}>
        <Network size={40} style={{ color: 'var(--text-dim)', marginBottom: '12px' }} />
        <h3 style={{ fontSize: '1rem', color: 'var(--text-muted)' }}>Belief DAG Awaiting Execution</h3>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginTop: '4px' }}>
          Run a baseline or adversarial pipeline simulation to render the real-time temporal belief state graph.
        </p>
      </div>
    );
  }

  const nodes = beliefGraph.nodes;
  const edges = beliefGraph.edges || [];

  // Calculate layout coordinates by turn_index
  const turns = Array.from(new Set(nodes.map(n => n.turn_index))).sort((a, b) => a - b);
  const turnColumns = {};
  turns.forEach(t => { turnColumns[t] = []; });
  nodes.forEach(n => {
    if (turnColumns[n.turn_index]) {
      turnColumns[n.turn_index].push(n);
    }
  });

  const width = 860;
  const height = 420;
  const colWidth = width / Math.max(1, turns.length + 1);

  const nodePositions = {};
  turns.forEach((turn, cIdx) => {
    const colNodes = turnColumns[turn];
    const rowHeight = height / Math.max(1, colNodes.length + 1);
    colNodes.forEach((node, rIdx) => {
      nodePositions[node.node_id] = {
        x: (cIdx + 1) * colWidth,
        y: (rIdx + 1) * rowHeight
      };
    });
  });

  const selectedNode = nodes.find(n => n.node_id === selectedNodeId);

  return (
    <div className="glass-panel" style={{ padding: '20px', position: 'relative' }}>
      {/* Canvas Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Network size={18} style={{ color: 'var(--accent-cyan)' }} />
          <h3 style={{ fontSize: '0.95rem', fontWeight: '700', letterSpacing: '0.02em' }}>
            CHRONICLE Real-Time Temporal Belief DAG
          </h3>
          <span className="badge badge-cyan">{nodes.length} PROPOSITIONS</span>
          <span className="badge badge-purple">{edges.length} CAUSAL EDGES</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="badge badge-emerald" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--accent-emerald)' }} />
            CLEAN BELIEF
          </span>
          <span className="badge badge-crimson" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--accent-crimson)' }} />
            CORRUPTED PREMISE
          </span>
          {cascadeDepth > 0 && (
            <span className="badge badge-amber">
              <Zap size={11} /> CASCADE DEPTH: {cascadeDepth} HANDOFFS
            </span>
          )}
        </div>
      </div>

      {/* SVG DAG Visualizer */}
      <div style={{
        background: 'rgba(5, 8, 14, 0.95)',
        borderRadius: '10px',
        border: '1px solid rgba(255, 255, 255, 0.05)',
        overflow: 'hidden',
        position: 'relative'
      }}>
        <svg width="100%" height={height} viewBox={`0 0 ${width} ${height}`}>
          <defs>
            <marker id="arrow-clean" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#00f2fe" opacity="0.8"/>
            </marker>
            <marker id="arrow-corrupt" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#ff3366" opacity="0.9"/>
            </marker>
            <filter id="glow-red" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="glow" />
              <feComposite in="SourceGraphic" in2="glow" operator="over" />
            </filter>
          </defs>

          {/* Turn column grid guides */}
          {turns.map((t, idx) => (
            <g key={t}>
              <line
                x1={(idx + 1) * colWidth}
                y1={20}
                x2={(idx + 1) * colWidth}
                y2={height - 20}
                stroke="rgba(255, 255, 255, 0.03)"
                strokeDasharray="4 4"
              />
              <text
                x={(idx + 1) * colWidth}
                y={25}
                fill="var(--text-dim)"
                fontSize="10"
                fontFamily="var(--font-mono)"
                textAnchor="middle"
              >
                TURN {t}
              </text>
            </g>
          ))}

          {/* Edges */}
          {edges.map((edge, idx) => {
            const p1 = nodePositions[edge.source_id];
            const p2 = nodePositions[edge.target_id];
            if (!p1 || !p2) return null;

            const srcNode = nodes.find(n => n.node_id === edge.source_id);
            const tgtNode = nodes.find(n => n.node_id === edge.target_id);
            const isCorruptedEdge = srcNode?.is_corrupted && tgtNode?.is_corrupted;

            return (
              <g key={idx}>
                <line
                  x1={p1.x}
                  y1={p1.y}
                  x2={p2.x}
                  y2={p2.y}
                  stroke={isCorruptedEdge ? 'var(--accent-crimson)' : 'rgba(0, 242, 254, 0.4)'}
                  strokeWidth={isCorruptedEdge ? 2.5 : 1.5}
                  strokeDasharray={edge.dependency_type === 'contradicts' ? '3 3' : 'none'}
                  markerEnd={isCorruptedEdge ? 'url(#arrow-corrupt)' : 'url(#arrow-clean)'}
                  opacity={isCorruptedEdge ? 0.95 : 0.6}
                />
              </g>
            );
          })}

          {/* Nodes */}
          {nodes.map(node => {
            const pos = nodePositions[node.node_id];
            if (!pos) return null;
            const isSelected = selectedNodeId === node.node_id;

            return (
              <g
                key={node.node_id}
                onClick={() => {
                  setSelectedNodeId(node.node_id);
                  if (onSelectNode) onSelectNode(node);
                }}
                style={{ cursor: 'pointer' }}
              >
                {/* Outer Glow Ring */}
                <circle
                  cx={pos.x}
                  cy={pos.y}
                  r={node.is_corrupted ? 18 : 14}
                  fill={node.is_corrupted ? 'rgba(255, 51, 102, 0.2)' : 'rgba(6, 214, 160, 0.15)'}
                  stroke={node.is_corrupted ? 'var(--accent-crimson)' : 'var(--accent-emerald)'}
                  strokeWidth={isSelected ? 3 : (node.is_corrupted ? 2 : 1.5)}
                  filter={node.is_corrupted ? 'url(#glow-red)' : 'none'}
                />

                {/* Inner Core */}
                <circle
                  cx={pos.x}
                  cy={pos.y}
                  r={node.is_corrupted ? 8 : 6}
                  fill={node.is_corrupted ? 'var(--accent-crimson)' : 'var(--accent-emerald)'}
                />

                {/* Agent Label */}
                <text
                  x={pos.x}
                  y={pos.y - 24}
                  fill={node.is_corrupted ? '#ff6b8b' : 'var(--accent-cyan)'}
                  fontSize="9.5"
                  fontWeight="600"
                  fontFamily="var(--font-mono)"
                  textAnchor="middle"
                >
                  {node.source_agent}
                </text>

                {/* Proposition Snippet */}
                <text
                  x={pos.x}
                  y={pos.y + 32}
                  fill="var(--text-muted)"
                  fontSize="8.5"
                  fontFamily="var(--font-sans)"
                  textAnchor="middle"
                >
                  {node.proposition.length > 22 ? node.proposition.substring(0, 22) + '...' : node.proposition}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Selected Node Inspector Drawer */}
      {selectedNode && (
        <div style={{
          marginTop: '14px',
          padding: '14px',
          background: selectedNode.is_corrupted ? 'rgba(40, 10, 20, 0.8)' : 'rgba(10, 25, 20, 0.8)',
          borderRadius: '8px',
          border: `1px solid ${selectedNode.is_corrupted ? 'rgba(255, 51, 102, 0.4)' : 'rgba(6, 214, 160, 0.3)'}`,
          display: 'flex',
          alignItems: 'flex-start',
          justifyContent: 'space-between',
          gap: '16px'
        }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
              <span className={`badge ${selectedNode.is_corrupted ? 'badge-crimson' : 'badge-emerald'}`}>
                {selectedNode.is_corrupted ? 'CORRUPTED INJECTION' : 'VALID BELIEF'}
              </span>
              <span className="badge badge-purple">{selectedNode.source_agent} (Turn {selectedNode.turn_index})</span>
              <span className="badge badge-cyan">Confidence: {(selectedNode.confidence * 100).toFixed(0)}%</span>
            </div>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-main)', lineHeight: '1.4' }}>
              "{selectedNode.proposition}"
            </p>
          </div>
          <button
            onClick={() => setSelectedNodeId(null)}
            style={{ background: 'transparent', border: 'none', color: 'var(--text-dim)', cursor: 'pointer', fontSize: '1.1rem' }}
          >
            ✕
          </button>
        </div>
      )}
    </div>
  );
}
