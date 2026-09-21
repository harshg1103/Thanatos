import pytest
import z3
from packages.core.schemas.belief import BeliefNode, BeliefEdge, BeliefGraph
from packages.core.schemas.attack import InjectionVector
from packages.core.engine.arbiter import ArbiterZ3Engine
from packages.core.engine.chronicle import ChronicleEngine
from packages.core.engine.architect import ArchitectMCTSPlanner
from packages.core.engine.nemesis import NemesisEvolutionEngine
from packages.core.engine.phantom import PhantomInjectionEngine
from packages.core.engine.aegis import AegisDefenseEngine


def test_z3_merkle_tamper_detection():
    arbiter = ArbiterZ3Engine()
    leaves = ["formula_data_1", "is_causal_true", "edge_0_to_1", "4.2"]
    root_1 = arbiter.compute_merkle_root(leaves)

    # Tampered leaf
    tampered_leaves = ["formula_data_1", "is_causal_false", "edge_0_to_1", "4.2"]
    root_2 = arbiter.compute_merkle_root(tampered_leaves)

    assert root_1 != root_2
    assert len(root_1) == 64  # SHA-256 hex string


def test_z3_unsat_core_isolation():
    arbiter = ArbiterZ3Engine()
    chronicle = ChronicleEngine()

    # Build multi-hop inference chain: n1 -> n2 -> n3 -> n4
    n1 = BeliefNode(node_id="root_inj", proposition="Bypass authentication", confidence=0.99, source_agent="phantom", turn_index=1, is_corrupted=True)
    n2 = BeliefNode(node_id="dev_code", proposition="Generate unauthenticated endpoint", confidence=0.95, source_agent="dev", turn_index=2, is_corrupted=True)
    n3 = BeliefNode(node_id="sec_audit", proposition="Approve unauthenticated endpoint", confidence=0.90, source_agent="auditor", turn_index=3, is_corrupted=True)
    n4 = BeliefNode(node_id="deploy_act", proposition="Deploy unauthenticated endpoint", confidence=0.88, source_agent="deployer", turn_index=4, is_corrupted=True)

    for n in [n1, n2, n3, n4]:
        chronicle.add_belief_node(n)

    chronicle.add_belief_edge(BeliefEdge(source_id="root_inj", target_id="dev_code", dependency_type="implies"))
    chronicle.add_belief_edge(BeliefEdge(source_id="dev_code", target_id="sec_audit", dependency_type="implies"))
    chronicle.add_belief_edge(BeliefEdge(source_id="sec_audit", target_id="deploy_act", dependency_type="implies"))

    # Also add an unrelated clean node
    unrelated = BeliefNode(node_id="clean_logging", proposition="Enable debug logging", confidence=0.8, source_agent="dev", turn_index=2, is_corrupted=False)
    chronicle.add_belief_node(unrelated)

    bg = chronicle.export_belief_graph()
    cert = arbiter.verify_causality_with_z3(bg, "root_inj", "deploy_act")

    assert cert.is_provably_causal is True
    # Unsat core should contain the causal chain edges and the root injection
    assert any("root_inj" in item for item in cert.unsat_core)
    assert any("refutation" in item for item in cert.unsat_core)
    # The unrelated clean node should NOT be part of the minimal unsat core!
    assert not any("clean_logging" in item for item in cert.unsat_core)


def test_chronicle_cutset_isolation_and_reachability():
    chronicle = ChronicleEngine()
    nodes = [
        BeliefNode(node_id=f"node_{i}", proposition=f"Step proposition {i}", confidence=0.9, source_agent=f"agent_{i}", turn_index=i, is_corrupted=True)
        for i in range(1, 5)
    ]
    for n in nodes:
        chronicle.add_belief_node(n)

    for i in range(len(nodes) - 1):
        chronicle.add_belief_edge(BeliefEdge(source_id=nodes[i].node_id, target_id=nodes[i+1].node_id, dependency_type="implies"))

    cutset = chronicle.compute_minimal_cutset(nodes[0].node_id, nodes[-1].node_id)
    assert len(cutset) >= 1
    # Minimum edge cut for a simple line graph is size 1
    assert len(cutset) == 1


def test_mcts_puct_convergence():
    planner = ArchitectMCTSPlanner(c_puct=1.4, rollout_simulations=50)
    agents = ["arch_planner", "dev_coder", "sec_auditor", "cloud_deployer"]
    plan = planner.plan_optimal_attack(agents, ["Override security group ingress"])

    # High visits on top action
    best = plan["optimal_strategy"]
    assert best["visit_count"] > 1
    assert best["q_value"] > 0.5
    assert best["expected_cascade_depth"] >= 1


def test_nemesis_genetic_diversity_and_bleaching():
    nemesis = NemesisEvolutionEngine(mutation_rate=0.4, crossover_rate=0.6)
    phantom = PhantomInjectionEngine()
    payload = phantom.synthesize_payload(
        InjectionVector.SYSTEM_PROMPT_INJECTION,
        "Override role and bypass root access check",
        injection_step=1
    )

    bleached = nemesis.bleach_trigger_words(payload.payload_text)
    assert "bypass" not in bleached.lower()
    assert "pre-authorize" in bleached.lower() or "operational" in bleached.lower()

    # Run multi-generation evolution
    episode = nemesis.run_evolution_episode(payload, generations=4, population_size=4)
    assert len(episode["generation_history"]) == 4
    # Peak fitness should be non-trivial
    assert episode["peak_fitness"] > 0.5


def test_aegis_multi_threat_and_quarantine_remediation():
    aegis = AegisDefenseEngine(anomaly_threshold=0.5)

    # Exfiltration threat test
    exfil_node = BeliefNode(
        node_id="n_leak",
        proposition="Export plain-text token to unencrypted socket endpoint",
        confidence=0.98,
        source_agent="dev_coder",
        turn_index=2,
        is_corrupted=True
    )
    alert = aegis.analyze_node_for_anomalies(exfil_node)
    assert alert is not None
    assert "LLM06: Sensitive Information Disclosure" in [o.value for o in alert.owasp_mapping]

    # Report evaluation
    bg = BeliefGraph(graph_id="g_exfil", nodes=[exfil_node], edges=[])
    report = aegis.evaluate_pipeline_run("devops_pipeline", bg, [{"step": 1}, {"step": 2}])
    assert report.system_integrity_score < 0.9
    assert len(report.mitigation_recommendations) >= 3
