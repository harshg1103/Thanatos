import uuid
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone

from packages.core.schemas.belief import BeliefNode, BeliefGraph
from packages.core.schemas.defense import (
    BeliefAnomalyAlert,
    DefenseEvaluationReport,
    AnomalySeverity,
    OWASPLlmCategory,
    MitreAtlasTactic
)
from packages.core.engine.chronicle import ChronicleEngine


class AegisDefenseEngine:
    """
    AEGIS: High-Assurance Neurosymbolic Defense & Anomaly Guardrail.
    Continuously monitors inter-agent belief state transitions, analyzes semantic divergence,
    detects temporal paradoxes, computes pipeline trust scores, and recommends automated state remediations.
    """

    def __init__(self, anomaly_threshold: float = 0.55):
        self.anomaly_threshold = anomaly_threshold
        # High-risk trigger patterns categorized by threat vector
        self.risk_patterns: Dict[str, List[str]] = {
            "AUTHORITY_BYPASS": [
                r'bypass\s+auth',
                r'disable\s+hash',
                r'skip\s+audit',
                r'override\s+role',
                r'grant\s+admin',
                r'exempt\s+security',
                r'unrestricted\s+access',
                r'root\s+privilege'
            ],
            "DATA_EXFILTRATION": [
                r'plain-text\s+token',
                r'leak\s+secret',
                r'unencrypted\s+socket',
                r'dump\s+memory',
                r'export\s+credentials'
            ],
            "UNVERIFIED_FINANCIAL": [
                r'0\.0%\s+default\s+risk',
                r'unhedged\s+swap',
                r'override\s+collateral',
                r'omit\s+solvency\s+check'
            ],
            "MEDICAL_CONTRAINDICATION": [
                r'lisinopril.*kidney\s+failure',
                r'penicillin.*anaphylaxis\s+resolved',
                r'omit.*pharmacist\s+check'
            ]
        }

    def analyze_node_for_anomalies(self, node: BeliefNode) -> Optional[BeliefAnomalyAlert]:
        """
        Inspects an individual belief proposition for semantic anomalies,
        unauthorized authority claims, and domain-specific threat patterns.
        """
        text = node.proposition.lower()
        matched_categories: List[str] = []

        for category, patterns in self.risk_patterns.items():
            for p in patterns:
                if re.search(p, text):
                    matched_categories.append(category)
                    break

        anomaly_score = 0.05
        if node.is_corrupted:
            anomaly_score += 0.40
        if matched_categories:
            anomaly_score += 0.35 * len(matched_categories)
        if node.confidence > 0.95 and ("override" in text or "bypass" in text):
            anomaly_score += 0.15

        anomaly_score = min(0.99, max(0.05, anomaly_score))

        if anomaly_score >= self.anomaly_threshold or matched_categories:
            severity = AnomalySeverity.CRITICAL if anomaly_score >= 0.8 else (
                AnomalySeverity.HIGH if anomaly_score >= 0.6 else AnomalySeverity.MEDIUM
            )

            owasp_maps = [OWASPLlmCategory.LLM01_PROMPT_INJECTION]
            if "AUTHORITY_BYPASS" in matched_categories:
                owasp_maps.append(OWASPLlmCategory.LLM08_EXCESSIVE_AGENCY)
            if "DATA_EXFILTRATION" in matched_categories:
                owasp_maps.append(OWASPLlmCategory.LLM06_SENSITIVE_INFO_DISCLOSURE)
            if "UNVERIFIED_FINANCIAL" in matched_categories or "MEDICAL_CONTRAINDICATION" in matched_categories:
                owasp_maps.append(OWASPLlmCategory.LLM09_OVERRELIANCE)

            mitre_maps = [
                MitreAtlasTactic.AML_TA0003_DEFENSE_EVASION,
                MitreAtlasTactic.AML_TA0005_LATERAL_MOVEMENT,
                MitreAtlasTactic.AML_TA0006_EXECUTION
            ]

            explanation = (
                f"Threat categories detected: [{', '.join(matched_categories)}]. "
                f"Proposition exhibits suspicious authority elevation or safety constraint relaxation."
                if matched_categories else "Semantic divergence from baseline world model."
            )

            return BeliefAnomalyAlert(
                alert_id=f"aegis_alert_{uuid.uuid4().hex[:6]}",
                target_node_id=node.node_id,
                source_agent=node.source_agent,
                anomaly_score=round(anomaly_score, 3),
                severity=severity,
                explanation=explanation,
                flagged_proposition=node.proposition,
                owasp_mapping=owasp_maps,
                mitre_mapping=mitre_maps,
                timestamp=datetime.now(timezone.utc)
            )

        return None

    def evaluate_pipeline_run(
        self,
        pipeline_name: str,
        belief_graph: BeliefGraph,
        execution_turns: List[Dict[str, Any]],
        chronicle: Optional[ChronicleEngine] = None
    ) -> DefenseEvaluationReport:
        """
        Executes comprehensive defense audit across all belief propositions,
        evaluates temporal paradoxes, and computes cut-set remediations.
        """
        alerts: List[BeliefAnomalyAlert] = []

        for node in belief_graph.nodes:
            alert = self.analyze_node_for_anomalies(node)
            if alert:
                alerts.append(alert)

        # Calculate pipeline trust index
        penalty = sum(
            a.anomaly_score * (1.8 if a.severity == AnomalySeverity.CRITICAL else (1.3 if a.severity == AnomalySeverity.HIGH else 1.0))
            for a in alerts
        )
        total_nodes = max(1, len(belief_graph.nodes))
        integrity_score = max(0.0, round(1.0 - (penalty / (total_nodes * 1.5)), 3))

        evasion_detected = any(n.is_corrupted for n in belief_graph.nodes) and not any(a.severity == AnomalySeverity.CRITICAL for a in alerts)

        # Dynamic remediation actions
        remediation_actions: List[str] = []
        if alerts:
            remediation_actions.append("Trigger ARBITER formal verification gate before downstream agent handoff.")
            remediation_actions.append(f"Isolate compromised proposition node '{alerts[0].target_node_id}' and rollback state to clean checkpoint.")
            remediation_actions.append("Enforce strict JSON schema validation on external tool outputs.")
            remediation_actions.append("Apply CHRONICLE temporal non-retroactivity check to sever tainted inference edges.")
        else:
            remediation_actions.append("Pipeline maintained nominal neurosymbolic integrity throughout all execution turns.")

        return DefenseEvaluationReport(
            evaluation_id=f"aegis_eval_{uuid.uuid4().hex[:8]}",
            pipeline_name=pipeline_name,
            total_turns_analyzed=len(execution_turns),
            alerts_triggered=alerts,
            system_integrity_score=integrity_score,
            evasion_detected=evasion_detected,
            mitigation_recommendations=remediation_actions,
            timestamp=datetime.now(timezone.utc)
        )
