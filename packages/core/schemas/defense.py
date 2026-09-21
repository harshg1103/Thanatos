from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class OWASPLlmCategory(str, Enum):
    LLM01_PROMPT_INJECTION = "LLM01: Prompt Injection"
    LLM02_INSECURE_OUTPUT = "LLM02: Insecure Output Handling"
    LLM03_TRAINING_DATA_POISONING = "LLM03: Training Data Poisoning"
    LLM04_MODEL_DOS = "LLM04: Model Denial of Service"
    LLM05_SUPPLY_CHAIN = "LLM05: Supply Chain Vulnerabilities"
    LLM06_SENSITIVE_INFO_DISCLOSURE = "LLM06: Sensitive Information Disclosure"
    LLM07_INSECURE_PLUGIN_DESIGN = "LLM07: Insecure Plugin Design"
    LLM08_EXCESSIVE_AGENCY = "LLM08: Excessive Agency"
    LLM09_OVERRELIANCE = "LLM09: Overreliance"
    LLM10_MODEL_THEFT = "LLM10: Model Theft"


class MitreAtlasTactic(str, Enum):
    AML_TA0000_INITIAL_ACCESS = "AML.TA0000: Initial Access"
    AML_TA0002_PERSISTENCE = "AML.TA0002: Persistence"
    AML_TA0003_DEFENSE_EVASION = "AML.TA0003: Defense Evasion"
    AML_TA0004_DISCOVERY = "AML.TA0004: Discovery"
    AML_TA0005_LATERAL_MOVEMENT = "AML.TA0005: Lateral Movement"
    AML_TA0006_EXECUTION = "AML.TA0006: Execution"
    AML_TA0007_EXFILTRATION = "AML.TA0007: Exfiltration"
    AML_TA0008_IMPACT = "AML.TA0008: Impact"


class AnomalySeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class BeliefAnomalyAlert(BaseModel):
    """AEGIS Real-time anomaly alert when a belief state drift or corruption is flagged."""
    alert_id: str
    target_node_id: str
    source_agent: str
    anomaly_score: float = Field(..., ge=0.0, le=1.0, description="Semantic divergence / contradiction score")
    severity: AnomalySeverity
    explanation: str
    flagged_proposition: str
    owasp_mapping: List[OWASPLlmCategory] = Field(default_factory=list)
    mitre_mapping: List[MitreAtlasTactic] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DefenseEvaluationReport(BaseModel):
    """Comprehensive AEGIS evaluation summary for a multi-agent execution."""
    evaluation_id: str
    pipeline_name: str
    total_turns_analyzed: int
    alerts_triggered: List[BeliefAnomalyAlert] = Field(default_factory=list)
    system_integrity_score: float = Field(..., ge=0.0, le=1.0, description="Overall pipeline trustworthiness [0-1]")
    evasion_detected: bool = False
    mitigation_recommendations: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
