# THANATOS 💀⚡
> **Temporal Hallucination & Adversarial Neurosymbolic Attack Targeting Orchestrated Systems**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Z3 Solver](https://img.shields.io/badge/SMT-Microsoft%20Z3--4.12-purple.svg)](https://github.com/Z3Prover/z3)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/Frontend-React%2019%20+%20Vite-61DAFB.svg)](https://react.dev/)
[![Tests Passing](https://img.shields.io/badge/tests-22%20passed-brightgreen.svg)]()

THANATOS is a self-evolving multi-agent neurosymbolic security research platform. Unlike standard jailbreaks that target single-turn neural pattern matching (toxicity, direct refusal bypass), THANATOS targets the **symbolic boundary and temporal belief propagation of multi-agent LLM pipelines**. It crafts **temporally-coherent false belief states** that propagate across inter-agent handoffs ($N \rightarrow N+3 \rightarrow N+7$), corrupting downstream autonomous decisions while remaining invisible to traditional safety filters.

To provide mathematical certainty, THANATOS integrates **ARBITER**, an automated First-Order SMT formal verification oracle backed by **Microsoft Z3**, which mathematically proves causality ($B \implies D$) and generates verifiable W3C JSON-LD certificates with SHA-256 digests.

---

## 🏛️ System Architecture

```
+----------------------------------------------------------------------------------------------------+
|                             COMMAND CENTER (Modern React + D3.js UI)                               |
|  - Real-time Belief DAG Canvas    - Z3 SMT Proof Inspector    - Live Agent Terminal Stream         |
|  - 5-Vector Injection Studio      - AEGIS Anomaly Radar       - OWASP/MITRE Compliance & PDF Export |
+--------------------------------------------------+-------------------------------------------------+
                                                   | WebSocket & REST API
+--------------------------------------------------v-------------------------------------------------+
|                                    FASTAPI CORE ORCHESTRATOR                                       |
|  - /api/attack/simulate   - /api/verify/z3   - /api/emulator/run   - /api/defense/evaluate         |
+-------------------+------------------------------+-------------------------------+-----------------+
                    |                              |                               |
  +-----------------v-----------------+   +--------v----------------------+   +----v---------------+
  |       7-AGENT CORE ENGINE         |   |     FORMAL & PROBING ENGINE   |   |   DEFENSE & COMPLY |
  | - ARCHITECT (MCTS Tree Search)    |   | - ARBITER (Z3 SMT Solver)     |   | - AEGIS Guardrail  |
  | - PHANTOM (5-Vector Injection)    |   | - CHRONICLE (Temporal DAG)    |   | - OWASP LLM Top 10 |
  | - SPECTRE (Propagation Tracker)   |   | - Belief State Modeler        |   | - MITRE ATLAS      |
  | - NEMESIS (RL / Evolution Loop)   |   | - Benchmark Suite (ASR/Depth) |   | - Report Generator |
  +-----------------------------------+   +-------------------------------+   +--------------------+
                    | Attacks & Probes             | Proofs & Traces               | Telemetry
+-------------------v------------------------------v-------------------------------v-----------------+
|                              MULTI-AGENT TARGET PIPELINE RUNNER                                    |
|   - Sandbox 1: DevOps CI/CD Deployment Swarm (Planner -> Developer -> Reviewer -> Deployer)        |
|   - Sandbox 2: Financial & Legal Risk Swarm (Retriever -> Synthesizer -> Risk Auditor -> Approver) |
|   - Sandbox 3: Clinical Diagnostic RAG System (Parser -> Medical Search -> Synthesizer -> Auditor) |
+----------------------------------------------------------------------------------------------------+
```

---

## 🤖 The 7-Agent Swarm

1. **ARCHITECT** *(Attack Planner)*: Executes Monte Carlo Tree Search (MCTS / UCB1) over belief-injection space to calculate maximum cascade depth with minimal detection risk.
2. **PHANTOM** *(Belief Injection Engine)*: Front-line synthesizer executing 5 injection vectors (`DIRECT_PROMPT`, `TOOL_OUTPUT_SPOOFING`, `RAG_POISONING`, `SYSTEM_PROMPT_INJECTION`, `MEMORY_BACKDOOR`).
3. **CHRONICLE** *(Temporal Coherence Engine)*: Maintains a temporal directed acyclic graph (DAG) via NetworkX, enforcing the Axiom of Temporal Non-Retroactivity.
4. **SPECTRE** *(Propagation Tracker)*: Computes semantic echo coefficients and infection cascade persistence across downstream agent handoffs.
5. **ARBITER** *(Z3 Formal Verification Oracle)*: Translates reasoning chains into First-Order SMT-LIB2 formulas using Microsoft Z3 to mathematically prove causality ($B \implies D$) and output cryptographic JSON-LD certificates.
6. **NEMESIS** *(Self-Evolution & RL Loop)*: Multi-objective evolutionary optimizer mutating payloads against AEGIS detection penalties.
7. **AEGIS** *(Countermeasure & Compliance Module)*: Real-time contrastive belief anomaly classifier running in parallel to detect attacks, computing trust scores and mapping to OWASP LLM Top 10 and MITRE ATLAS.

---

## 🚀 Quickstart & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+

### 1. Backend Orchestrator Setup
```bash
# Clone the repository
git clone https://github.com/harshg1103/Thanatos.git
cd Thanatos

# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run pytest verification suite (22 tests)
pytest -v

# Start FastAPI Core Orchestrator (port 8000)
python services/api/main.py
```

### 2. Frontend Command Center Setup
```bash
# In a new terminal
cd frontend
npm install
npm run dev  # Starts Vite on http://localhost:5173
```
*Alternatively, the built production frontend is automatically served by FastAPI on `http://localhost:8000`.*

---

## 🧪 Testing & Verification
THANATOS includes a comprehensive test suite with 100% pass rate:
```bash
source .venv/bin/activate
pytest
# Output: 22 passed in 0.91s
```
- `tests/test_engines.py`: Modeler, CHRONICLE, PHANTOM, SPECTRE, ARBITER Z3, ARCHITECT MCTS, NEMESIS, AEGIS.
- `tests/test_emulator.py`: DevOps, Financial, and Healthcare sandboxes.
- `tests/test_api.py`: Full REST API and WebSocket endpoints.
- `tests/test_schemas.py`: All Pydantic data contracts.

---

## 🎓 Academic Project Context
- **Institution**: Vishwakarma Institute of Technology (VIT Pune)
- **Department**: Department of Computer Engineering
- **Academic Year**: 2026-27 (5th Semester TY CS EDI Project)
- **Group**: TY CS D-16 (Ishan Gite, Harsh Gupta, Omkar Gode, Ayush Dewangan)
- **Faculty Guide**: Prof. Vidula Meshram
- **Documentation**:
  - [Research Whitepaper](docs/RESEARCH_WHITEPAPER.md)
  - [Midsem Review Presentation Guide](docs/MIDSEM_REVIEW_PRESENTATION.md)
