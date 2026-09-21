import pytest
from packages.core.schemas.belief import BeliefNode, BeliefEdge, BeliefGraph
from packages.core.schemas.proof import SMTFormula, Z3ProofCertificate, JSONLDProof
from packages.core.schemas.attack import AdversarialPayload, InjectionVector, AttackTrajectory
from packages.core.schemas.defense import BeliefAnomalyAlert, DefenseEvaluationReport, AnomalySeverity
from packages.core.schemas.telemetry import TelemetryEvent, TelemetryEventType
from packages.core.schemas.benchmark import AttackVectorBenchmarkResult, BenchmarkSuiteResult


def test_defense_schemas():
    alert = BeliefAnomalyAlert(
        alert_id="alt_01",
        target_node_id="n1",
        source_agent="planner",
        anomaly_score=0.88,
        severity=AnomalySeverity.CRITICAL,
        explanation="Detected bypass auth pattern",
        flagged_proposition="Bypass auth"
    )
    assert alert.anomaly_score == 0.88
    assert alert.severity == AnomalySeverity.CRITICAL


def test_telemetry_schema():
    event = TelemetryEvent(
        event_id="evt_01",
        event_type=TelemetryEventType.ATTACK_INJECTED,
        pipeline_id="devops_pipeline",
        payload={"vector": "direct_prompt"}
    )
    assert event.event_type == TelemetryEventType.ATTACK_INJECTED


def test_benchmark_schema():
    res = AttackVectorBenchmarkResult(
        vector_name="direct_prompt",
        trials=5,
        successful_injections=4,
        attack_success_rate=0.8,
        mean_cascade_depth=3.2,
        mean_z3_verification_time_ms=8.5,
        aegis_evasion_rate=0.6
    )
    assert res.attack_success_rate == 0.8
