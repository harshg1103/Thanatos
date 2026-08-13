# THANATOS 💀⚡
> **Temporal Hallucination & Adversarial Neurosymbolic Attack Targeting Orchestrated Systems**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Z3 Solver](https://img.shields.io/badge/SMT-Z3--4.12-purple.svg)](https://github.com/Z3Prover/z3)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-green.svg)](https://github.com/langchain-ai/langgraph)

THANATOS is a self-evolving multi-agent neurosymbolic security research platform. Unlike standard jailbreaks that target single-turn neural pattern matching (toxicity, direct refusal bypass), THANATOS targets the **symbolic boundary of multi-agent LLM pipelines**. It plants **temporally-coherent false belief states** into shared agent memory/context that are contextually plausible and invisible to traditional neural safety filters. These corrupted beliefs propagate across agent handoffs ($N \rightarrow N+3 \rightarrow N+7 \rightarrow N+12$), corrupting downstream autonomous decisions.

---

## 🏛️ Architecture Overview

```
+----------------------------------------------------------------------------------------------------+
|                                    LIVE DASHBOARD (Next.js 15 + D3.js)                             |
|  - Real-time Attack Genealogy Graph   - Z3 Proof Viewer   - AEGIS Anomaly Stream   - OWASP PDF Exporter |
+--------------------------------------------------+-------------------------------------------------+
                                                   | WebSocket / REST API
+--------------------------------------------------v-------------------------------------------------+
|                                    FASTAPI CORE ORCHESTRATOR                                       |
+-------------------+------------------------------+-------------------------------+-----------------+
|                   |                              |                               |                 |
|  +----------------v-----------------+   +--------v----------------------+   +----v---------------+ |
|  |     7-AGENT ATTACK SWARM         |   |     FORMAL & PROBING ENGINE   |   |   DEFENSE MIDDLEWARE | |
|  | - ARCHITECT (MCTS Planner)       |   | - ARBITER (Z3 Formal Solver)  |   | - AEGIS Anomalies | |
|  | - PHANTOM (5-Vector Injection)   |   | - CHRONICLE (Temporal DAG)    |   | - Compliance Mapper| |
|  | - NEMESIS (PPO Self-Evolution)   |   | - Belief State Modeler (DSPy) |   |   (OWASP/MITRE)    | |
|  | - SPECTRE (Propagation Tracker)  |   +-------------------------------+   +--------------------+ |
|  +----------------------------------+                                                              |
+--------------------------------------------------+-------------------------------------------------+
                                                   | Attacks & Probes
+--------------------------------------------------v-------------------------------------------------+
|                              TARGET PIPELINE EMULATOR (Docker Sandbox)                            |
|       - Sandbox 1: Code Assistant Agent   - Sandbox 2: Research Swarm   - Sandbox 3: RAG Chatbot     |
+----------------------------------------------------------------------------------------------------+
```

---

## 🤖 The 7-Agent Swarm

1. **ARCHITECT** *(Attack Planner)*: Uses Monte Carlo Tree Search over belief-injection space to calculate maximum cascade depth.
2. **PHANTOM** *(Belief Injection Agent)*: Front-line attacker executing 5 injection vectors (Direct prompt, Tool spoofing, RAG poison, System prompt, Memory backdoor).
3. **CHRONICLE** *(Temporal Coherence Engine)*: Maintains a temporal belief DAG to prevent logical paradoxes across turns.
4. **SPECTRE** *(Propagation Tracker)*: Tracks belief echoes in downstream agent outputs, building real-time attack genealogy graphs.
5. **ARBITER** *(Z3 Verification Oracle)*: Translates agent reasoning into SMT formulas using Microsoft Z3 to formally prove causality ($B \rightarrow D$) and output JSON-LD certificates.
6. **NEMESIS** *(RL Self-Evolution)*: PPO loop (Stable-Baselines3 + LanceDB memory) optimizing attack strategies over training episodes.
7. **AEGIS** *(Countermeasure Module)*: Contrastive learning belief anomaly classifier running in parallel to detect attacks in real time.

---

## 🚀 Quickstart & Scaffolding Setup

### Prerequisites
- Python 3.11+
- Docker & Docker Desktop (for sandboxed target emulation)
- Node.js 18+ (for dashboard command center)

### Installation
```bash
# Clone the repository
git clone https://github.com/your-username/thanatos.git
cd thanatos

# Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e packages/core
```

---

## 🎓 Academic Project Context
- **Institution**: Vishwakarma Institute of Technology (VIT Pune)
- **Academic Year**: 2026-27 (5th Semester CS Engineering EDI Project)
- **Group**: TY CS D-16 (Ishan Gite, Harsh Gupta, Omkar Gode, Ayush Dewangan)
- **Guide**: Prof. Vidula Meshram
