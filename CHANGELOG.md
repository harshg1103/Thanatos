# Changelog - Project THANATOS

All notable changes to this project are documented in this file.

## [1.0.0] - 2026-09-19 (Mid-Semester Milestone Release)

### Added
- **Core Neurosymbolic Engines (`packages/core/engine/`)**:
  - `belief_modeler.py`: Neurosymbolic proposition extraction and causal dependency inference.
  - `chronicle.py`: NetworkX temporal belief DAG with paradox detection and blast radius analysis.
  - `phantom.py`: 5-vector adversarial payload synthesis (`DIRECT_PROMPT`, `TOOL_OUTPUT_SPOOFING`, `RAG_POISONING`, `SYSTEM_PROMPT_INJECTION`, `MEMORY_BACKDOOR`).
  - `spectre.py`: Semantic echo and belief propagation tracker.
  - `arbiter.py`: Microsoft Z3 SMT solver proving formal entailment ($B \implies D$) with JSON-LD certificate emitter.
  - `architect.py`: Monte Carlo Tree Search (MCTS / UCB1) attack planner.
  - `nemesis.py`: Evolutionary optimization and PPO-inspired payload mutator.
  - `aegis.py`: Real-time anomaly detector and system integrity analyzer.
  - `compliance.py`: OWASP Top 10 for LLMs and MITRE ATLAS taxonomy mapper.
  - `benchmark.py`: Empirical quantitative benchmarking suite.
- **Realistic Multi-Agent Target Emulator (`emulators/`)**:
  - Replaced mock runner with dynamic multi-agent pipeline engine.
  - Added 3 distinct sandboxes: DevOps CI/CD Swarm, Financial Risk Swarm, Healthcare Diagnostic RAG.
- **FastAPI Core Orchestrator (`services/api/`)**:
  - Added REST routers for attack simulation, Z3 formal proofs, AEGIS defenses, benchmarks, and audit reports.
  - Added real-time WebSocket `/ws/telemetry` streaming.
- **Frontend Command Center (`frontend/`)**:
  - Modern React 19 + Vite dashboard with dark cyber-research design system.
  - Interactive D3/SVG Belief DAG canvas with real-time node corruption visualization.
  - ARBITER Z3 Proof Inspector with SMT-LIB2 viewer and JSON-LD certificate download.
  - Live Agent Terminal with turn-by-turn scratchpad reasoning and handoffs.
  - AEGIS Defense Radar and OWASP/MITRE taxonomy cards.
  - Printable / Exportable Security Audit Report modal.
- **Academic Package (`docs/`)**:
  - `RESEARCH_WHITEPAPER.md`: Formal theoretical foundation and math formulation.
  - `MIDSEM_REVIEW_PRESENTATION.md`: Slide deck guide and viva defense preparation.
- **Test Suite (`tests/`)**:
  - 22 comprehensive unit and integration tests with 100% pass rate.
