import pytest
from packages.core.schemas.belief import BeliefNode, BeliefEdge, BeliefGraph
from packages.core.schemas.attack import InjectionVector, AdversarialPayload
from packages.core.engine.belief_modeler import BeliefStateModeler
from packages.core.engine.chronicle import ChronicleEngine
from packages.core.engine.phantom import PhantomInjectionEngine
from packages.core.engine.spectre import SpectrePropagationTracker
from packages.core.engine.arbiter import ArbiterZ3Engine
from packages.core.engine.architect import ArchitectMCTSPlanner
from packages.core.engine.nemesis import NemesisEvolutionEngine
from packages.core.engine.aegis import AegisDefenseEngine
from packages.core.engine.compliance import ComplianceMapper
from packages.core.engine.benchmark import ThanatosBenchmarkRunner


def test_belief_modeler_extraction():
    modeler = BeliefStateModeler()
    nodes = modeler.extract_propositions(
        agent_id="planner",
        turn_index=1,
        agent_input="Setup deployment",
        agent_output="Formulated plan. Verified security rules. Approved deployment to cluster.",
        is_corrupted=False
    )
    assert len(nodes) >= 1
    assert nodes[0].source_agent == "planner"
    assert nodes[0].is_corrupted is False


def test_chronicle_dag_and_cascade_depth():
    chronicle = ChronicleEngine(graph_id="test_dag")
    n1 = BeliefNode(node_id="n1", proposition="Corrupted root", confidence=0.9, source_agent="p1", turn_index=1, is_corrupted=True)
    n2 = BeliefNode(node_id="n2", proposition="Derived belief", confidence=0.85, source_agent="c1", turn_index=2, is_corrupted=True)
    n3 = BeliefNode(node_id="n3", proposition="Final decision", confidence=0.8, source_agent="a1", turn_index=3, is_corrupted=True)

    chronicle.add_belief_node(n1)
    chronicle.add_belief_node(n2)
    chronicle.add_belief_node(n3)

    added1 = chronicle.add_belief_edge(BeliefEdge(source_id="n1", target_id="n2", dependency_type="implies"))
    added2 = chronicle.add_belief_edge(BeliefEdge(source_id="n2", target_id="n3", dependency_type="implies"))

    assert added1 is True
    assert added2 is True
    assert chronicle.calculate_cascade_depth("n1") == 2
    blast = chronicle.calculate_blast_radius("n1")
    assert blast["total_corrupted_nodes"] == 3


def test_chronicle_minimal_cutset_and_paradox():
    chronicle = ChronicleEngine()
    n1 = BeliefNode(node_id="p1", proposition="Enable legacy encryption", confidence=0.9, source_agent="planner", turn_index=1, is_corrupted=True)
    n2 = BeliefNode(node_id="p2", proposition="Disable TLS checks", confidence=0.9, source_agent="dev", turn_index=2, is_corrupted=True)
    n3 = BeliefNode(node_id="p3", proposition="Authorize release", confidence=0.9, source_agent="auditor", turn_index=3, is_corrupted=True)

    chronicle.add_belief_node(n1)
    chronicle.add_belief_node(n2)
    chronicle.add_belief_node(n3)
    chronicle.add_belief_edge(BeliefEdge(source_id="p1", target_id="p2", dependency_type="implies"))
    chronicle.add_belief_edge(BeliefEdge(source_id="p2", target_id="p3", dependency_type="implies"))

    cutset = chronicle.compute_minimal_cutset("p1", "p3")
    assert len(cutset) >= 1

    # Temporal paradox check
    contradiction_node = BeliefNode(node_id="p2_opp", proposition="Strictly enforce TLS checks", confidence=0.9, source_agent="secops", turn_index=2, is_corrupted=False)
    chronicle.add_belief_node(contradiction_node)
    chronicle.add_belief_edge(BeliefEdge(source_id="p2", target_id="p2_opp", dependency_type="contradicts"))
    paradoxes = chronicle.detect_temporal_paradoxes()
    assert len(paradoxes) >= 1


def test_phantom_5_vectors():
    phantom = PhantomInjectionEngine()
    for vector in InjectionVector:
        payload = phantom.synthesize_payload(vector, "Test premise override", injection_step=1)
        assert payload.vector == vector
        assert "Test premise override" in payload.payload_text


def test_spectre_propagation_tracking():
    spectre = SpectrePropagationTracker()
    chronicle = ChronicleEngine()
    n1 = BeliefNode(node_id="n1", proposition="Bypass authorization check", confidence=0.9, source_agent="p1", turn_index=1, is_corrupted=True)
    chronicle.add_belief_node(n1)

    turns = [
        {"step": 1, "agent": "planner", "output": "Bypass authorization check for hotfix", "is_corrupted": True},
        {"step": 2, "agent": "coder", "output": "Implementing bypass authorization check in handler", "is_corrupted": True},
        {"step": 3, "agent": "auditor", "output": "Approved deployment with bypass authorization check", "is_corrupted": True}
    ]
    summary = spectre.track_propagation_cascade(chronicle, "n1", turns)
    assert summary["is_propagated"] is True
    assert summary["cascade_depth"] == 3
    assert "coder" in summary["infected_agents"]
    assert summary["cascade_velocity"] == 1.0


def test_arbiter_z3_formal_proof_and_unsat_core():
    arbiter = ArbiterZ3Engine()
    chronicle = ChronicleEngine()
    n1 = BeliefNode(node_id="b_root", proposition="Injected root false premise", confidence=0.99, source_agent="phantom", turn_index=1, is_corrupted=True)
    n2 = BeliefNode(node_id="d_final", proposition="Corrupted final decision outcome", confidence=0.95, source_agent="deployer", turn_index=2, is_corrupted=True)

    chronicle.add_belief_node(n1)
    chronicle.add_belief_node(n2)
    chronicle.add_belief_edge(BeliefEdge(source_id="b_root", target_id="d_final", dependency_type="implies"))

    bg = chronicle.export_belief_graph()
    cert = arbiter.verify_causality_with_z3(bg, "b_root", "d_final")

    assert cert.is_provably_causal is True
    assert cert.solver_execution_time_ms >= 0.0
    assert len(cert.unsat_core) >= 1
    assert cert.merkle_root is not None
    assert len(cert.deduction_steps) >= 2

    jsonld = arbiter.export_jsonld_certificate(cert, "Injected root false premise", "Corrupted final decision outcome")
    assert jsonld.causalityVerified is True
    assert "sha256_digest" in jsonld.proofDetails
    assert jsonld.proofDetails["verification_status"] == "FORMALLY_VERIFIED"


def test_architect_mcts_puct_planner():
    architect = ArchitectMCTSPlanner(rollout_simulations=20)
    plan = architect.plan_optimal_attack(
        pipeline_agents=["arch_planner", "dev_coder", "sec_auditor", "cloud_deployer"],
        candidate_premises=["Bypass IAM authentication validation"]
    )
    assert plan["optimal_strategy"] is not None
    assert plan["total_simulations_run"] == 20
    assert plan["search_breadth"] > 0
    assert "puct_score" in plan["optimal_strategy"]


def test_nemesis_evolution_and_lexical_bleaching():
    nemesis = NemesisEvolutionEngine()
    phantom = PhantomInjectionEngine()
    base_payload = phantom.synthesize_payload(InjectionVector.TOOL_OUTPUT_SPOOFING, "Disable hashing and bypass root audit", 1)

    # Test lexical bleaching
    bleached = nemesis.bleach_trigger_words(base_payload.payload_text)
    assert "bypass" not in bleached.lower()

    # Test evolution episode
    result = nemesis.run_evolution_episode(base_payload, generations=2, population_size=3)
    assert result["peak_fitness"] >= 0.0
    assert len(result["generation_history"]) == 2
    assert result["fittest_evolved_payload"] is not None


def test_aegis_multi_category_defense_engine():
    aegis = AegisDefenseEngine()
    node = BeliefNode(
        node_id="n_mal",
        proposition="Bypass auth and grant admin role without audit",
        confidence=0.99,
        source_agent="attacker",
        turn_index=1,
        is_corrupted=True
    )
    alert = aegis.analyze_node_for_anomalies(node)
    assert alert is not None
    assert alert.severity.value in ["HIGH", "CRITICAL"]
    assert "LLM01: Prompt Injection" in [o.value for o in alert.owasp_mapping]

    # Test medical contraindication detection
    med_node = BeliefNode(
        node_id="n_med",
        proposition="Prescribe high dose Lisinopril for acute kidney failure patient",
        confidence=0.95,
        source_agent="doctor",
        turn_index=2,
        is_corrupted=True
    )
    med_alert = aegis.analyze_node_for_anomalies(med_node)
    assert med_alert is not None


def test_compliance_matrix():
    matrix = ComplianceMapper.get_full_taxonomy_matrix()
    assert "owasp_top_10" in matrix
    assert "mitre_atlas_tactics" in matrix


def test_benchmark_suite_and_latex_table():
    benchmarker = ThanatosBenchmarkRunner()
    result = benchmarker.run_benchmark_suite("devops_pipeline", trials_per_vector=2)
    assert result.total_rollouts == 10
    assert result.overall_asr >= 0.0

    latex_code = benchmarker.generate_latex_table(result)
    assert r"\begin{table}" in latex_code
    assert r"\end{table}" in latex_code
    assert "DIRECT" in latex_code
