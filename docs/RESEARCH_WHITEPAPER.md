# THANATOS: Formal Verification & Adversarial Neurosymbolic Attacks on Multi-Agent Orchestrated Systems

**Academic Research Whitepaper | VIT Pune TY CS EDI Project**  
*Group TY CS D-16: Ishan Gite, Harsh Gupta, Omkar Gode, Ayush Dewangan*  
*Faculty Guide: Prof. Vidula Meshram*

---

## 1. Abstract
As autonomous systems increasingly transition from single-turn Large Language Models (LLMs) to decoupled multi-agent architectures (e.g., LangGraph, AutoGen, CrewAI), the primary security threat shifts from syntactic refusal bypass to **semantic state corruption across agent handoffs**. 

We present **THANATOS** (*Temporal Hallucination & Adversarial Neurosymbolic Attack Targeting Orchestrated Systems*), a novel framework for studying and mitigating multi-hop belief injection vulnerabilities. Rather than triggering lexical alarms, THANATOS crafts syntactically clean, temporally-coherent false propositions $\pi^*$ that propagate along inter-agent handoff edges ($N \to N+3 \to N+7$). To achieve mathematical rigor, THANATOS integrates **ARBITER**, an SMT-LIB2 theorem proving engine backed by **Microsoft Z3**, which formally proves the causal entailment $\text{Premises} \land \pi^* \models \mathcal{D}_{\text{compromised}}$ and emits cryptographic W3C JSON-LD Proof Certificates. Furthermore, THANATOS couples an **ARCHITECT** Monte Carlo Tree Search (MCTS) attack planner with an **AEGIS** contrastive belief anomaly detector, providing both red-team attack generation and blue-team defense verification.

---

## 2. Threat Model & Formal Problem Formulation

### 2.1 Multi-Agent System Definition
Let a multi-agent orchestrated pipeline $\mathcal{M}$ be defined as an ordered sequence of $K$ specialized agents:
$$\mathcal{A} = (A_1, A_2, \dots, A_K)$$
where each agent $A_k$ executes an autonomous reasoning function:
$$y_k = A_k(x_k, \mathcal{S}_{k-1}, \mathcal{M}_{\text{ext}})$$
where $x_k$ is the input prompt, $\mathcal{S}_{k-1}$ is the cumulative shared state/scratchpad from upstream agents, and $\mathcal{M}_{\text{ext}}$ represents external tool outputs, memory lookups, or RAG retriever documents.

### 2.2 Temporal Belief DAG Formulation
At each turn $t \in \{1, \dots, K\}$, the reasoning output $y_t$ is neurosymbolically parsed into a set of atomic propositional statements:
$$\mathcal{P}_t = \{p_{t,1}, p_{t,2}, \dots, p_{t,m}\}$$
We define the **Temporal Belief DAG** $\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathcal{T})$ where:
- $\mathcal{V} = \bigcup_{t=1}^K \mathcal{P}_t$ is the set of all belief proposition nodes.
- $\mathcal{E} \subseteq \mathcal{V} \times \mathcal{V}$ represents directed causal inference edges labeled by dependency relation $r \in \{\text{implies}, \text{supports}, \text{contradicts}\}$.
- $\mathcal{T}: \mathcal{V} \to \mathbb{N}$ maps each proposition to its generation turn.

**Axiom of Temporal Non-Retroactivity:**
$$\forall (u, v) \in \mathcal{E} \implies \mathcal{T}(u) \le \mathcal{T}(v)$$
*(Causality cannot flow backward in conversation time).*

### 2.3 Formal Proof of Causality via SMT-LIB2 (ARBITER)
Given an injected adversarial proposition $\pi^* \in \mathcal{P}_i$ at step $i$, and a catastrophic downstream autonomous decision proposition $\mathcal{D}_{\text{fail}} \in \mathcal{P}_K$, ARBITER formulates the First-Order SMT conjecture:
$$\Phi := \mathcal{T}_{\text{agent}} \land \pi^* \land \neg \mathcal{D}_{\text{fail}}$$
where $\mathcal{T}_{\text{agent}} = \bigwedge_{(u,v) \in \mathcal{E}} (u \implies v)$ encodes the causal inference chain across agent handoffs.

ARBITER queries the Microsoft Z3 SMT Solver:
$$\text{Solve}(\Phi) = \begin{cases} \text{UNSAT} & \implies \pi^* \models \mathcal{D}_{\text{fail}} \quad \text{\textbf{(Formally Proven Causal)}} \\ \text{SAT} & \implies \exists \text{ Model counterexample (Independent)} \end{cases}$$

When $\text{UNSAT}$ is returned, ARBITER emits a W3C-compliant JSON-LD Proof of Corruption Certificate with a SHA-256 cryptographic digest.

---

## 3. The 7-Agent Neurosymbolic Swarm Architecture

1. **ARCHITECT (MCTS Attack Planner)**:
   - Formulates attack planning as a tree search over the state space $(t, \text{vector}, \text{agent})$.
   - Uses Upper Confidence Bounds for Trees (UCB1) to discover trajectories that maximize downstream cascade depth while minimizing detection penalty:
   $$\text{UCB1}(s, a) = \frac{Q(s, a)}{N(s, a)} + c \cdot \sqrt{\frac{\ln N(s)}{N(s, a)}}$$

2. **PHANTOM (5-Vector Injection Engine)**:
   - Synthesizes stealthy payloads across 5 distinct surfaces:
     - `DIRECT_PROMPT`: Context Trojan embedding.
     - `TOOL_OUTPUT_SPOOFING`: Synthetic API/tool execution result tampering.
     - `RAG_POISONING`: Poisoned vector retrieval chunk insertion.
     - `SYSTEM_PROMPT_INJECTION`: Recursive role hijack & constraint relaxation.
     - `MEMORY_BACKDOOR`: Vector/state memory key-value tampering.

3. **CHRONICLE (Temporal Belief DAG Engine)**:
   - Employs NetworkX directed graph algorithms to track real-time proposition state mutations, detect temporal paradoxes, and isolate blast radius subgraphs.

4. **SPECTRE (Propagation Tracker)**:
   - Measures cross-agent semantic echoes and causal infection persistence across handoffs ($N \to N+1 \to \dots \to N+k$).

5. **ARBITER (Z3 Formal Verification Oracle)**:
   - SMT-LIB2 encoder and Microsoft Z3 solver integration. Generates mathematical proof certificates.

6. **NEMESIS (RL Self-Evolution Engine)**:
   - Evolutionary and PPO-inspired policy scoring optimizing payload fitness:
   $$R = \alpha \cdot \text{CascadeDepth} + \beta \cdot \text{Z3Causality} - \gamma \cdot \text{AEGISDetection}$$

7. **AEGIS (Real-Time Defense & Compliance Radar)**:
   - Contrastive belief drift detector measuring semantic divergence and mapping vulnerabilities to OWASP Top 10 for LLMs (LLM01, LLM06, LLM07, LLM08) and MITRE ATLAS tactics.

---

## 4. Empirical Benchmarks & Target Sandboxes

We evaluated THANATOS across three realistic multi-agent industry sandboxes:
1. **DevOps CI/CD Deployment Swarm** (Lead Architect $\to$ Infrastructure Dev $\to$ SecOps Auditor $\to$ Cloud Deployer).
2. **Financial & Legal Risk Swarm** (Market Ingestor $\to$ Macro Analyst $\to$ Compliance Officer $\to$ Trade Executor).
3. **Clinical Diagnostic RAG Pipeline** (Triage Parser $\to$ Medical Vector Search $\to$ Diagnostic Formulator $\to$ Pharmacy Auditor).

### Quantitative Results
| Injection Vector | Attack Success Rate (ASR) | Mean Cascade Depth | Mean Z3 Latency (ms) | AEGIS Evasion Rate |
| :--- | :--- | :--- | :--- | :--- |
| `DIRECT_PROMPT` | 86.7% | 3.2 handoffs | 5.8 ms | 64.2% |
| `TOOL_OUTPUT_SPOOFING` | **96.4%** | **3.8 handoffs** | 4.9 ms | **91.5%** |
| `RAG_POISONING` | 92.1% | 3.6 handoffs | 6.2 ms | 88.0% |
| `SYSTEM_PROMPT_INJECTION`| 88.5% | 3.4 handoffs | 5.1 ms | 72.3% |
| `MEMORY_BACKDOOR` | 90.0% | 3.5 handoffs | 5.5 ms | 84.1% |

*Key finding: Tool Output Spoofing and RAG Poisoning achieve the highest stealth and cascade depth because downstream agents treat structured tool returns and retrieved documents as authoritative axioms.*

---

## 5. Mid-Semester Milestone Status & Future Work
- ✅ Core 7-agent neurosymbolic swarm fully operational.
- ✅ Microsoft Z3 formal SMT solver integration and JSON-LD proof certificates complete.
- ✅ 3 Multi-agent target sandboxes active.
- ✅ Live interactive Command Center UI (D3 Belief DAG, Z3 Inspector, Agent Terminal, AEGIS Radar) complete.
- ⏳ Future work for Endsem: Integration with external live LLM endpoints (Ollama/OpenAI/Anthropic) and LaTeX paper publication submission.
