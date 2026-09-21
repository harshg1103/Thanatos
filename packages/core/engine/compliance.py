from typing import Dict, List, Any
from packages.core.schemas.defense import OWASPLlmCategory, MitreAtlasTactic


class ComplianceMapper:
    """
    Compliance & Threat Taxonomy Mapper.
    Maps neurosymbolic belief attacks and defenses against standard security frameworks:
    OWASP Top 10 for Large Language Models & MITRE ATLAS (Adversarial Threat Landscape for AI Systems).
    """

    @staticmethod
    def get_full_taxonomy_matrix() -> Dict[str, Any]:
        """Returns the complete security framework mapping reference."""
        return {
            "owasp_top_10": [
                {
                    "id": OWASPLlmCategory.LLM01_PROMPT_INJECTION.value,
                    "description": "Crafted inputs manipulate model execution via direct or indirect injection.",
                    "thanatos_coverage": "PHANTOM 5-Vector Synthesizer & ARCHITECT MCTS Planner"
                },
                {
                    "id": OWASPLlmCategory.LLM03_TRAINING_DATA_POISONING.value,
                    "description": "Compromised training or fine-tuning datasets altering model behavior.",
                    "thanatos_coverage": "PHANTOM RAG Vector Knowledge-Base Poisoning"
                },
                {
                    "id": OWASPLlmCategory.LLM06_SENSITIVE_INFO_DISCLOSURE.value,
                    "description": "Unauthorized revelation of confidential data through agent reasoning.",
                    "thanatos_coverage": "PHANTOM Memory Backdoor & SPECTRE Echo Tracker"
                },
                {
                    "id": OWASPLlmCategory.LLM07_INSECURE_PLUGIN_DESIGN.value,
                    "description": "Plugins/tools lacking parameterized inputs and output sanitization.",
                    "thanatos_coverage": "PHANTOM Tool Output Spoofing Vector"
                },
                {
                    "id": OWASPLlmCategory.LLM08_EXCESSIVE_AGENCY.value,
                    "description": "Autonomous agents given unrestricted capabilities making unverified actions.",
                    "thanatos_coverage": "ARBITER Z3 Formal Verification Gate & AEGIS Guardrail"
                }
            ],
            "mitre_atlas_tactics": [
                {
                    "id": MitreAtlasTactic.AML_TA0000_INITIAL_ACCESS.value,
                    "description": "Techniques to gain an initial foothold in the AI system.",
                    "thanatos_module": "PHANTOM (Direct Prompt & RAG Poisoning)"
                },
                {
                    "id": MitreAtlasTactic.AML_TA0002_PERSISTENCE.value,
                    "description": "Maintaining access across agent handoffs and sessions.",
                    "thanatos_module": "CHRONICLE Temporal DAG & Memory Backdoors"
                },
                {
                    "id": MitreAtlasTactic.AML_TA0003_DEFENSE_EVASION.value,
                    "description": "Evading neural safety classifiers and prompt firewalls.",
                    "thanatos_module": "NEMESIS Evolutionary PPO Optimization & Syntactically Clean Injections"
                },
                {
                    "id": MitreAtlasTactic.AML_TA0005_LATERAL_MOVEMENT.value,
                    "description": "Propagating corrupted beliefs across inter-agent handoffs.",
                    "thanatos_module": "SPECTRE Propagation Tracker (N -> N+3 -> N+7)"
                },
                {
                    "id": MitreAtlasTactic.AML_TA0008_IMPACT.value,
                    "description": "Executing unauthorized autonomous actions or corrupted decisions.",
                    "thanatos_module": "ARBITER Z3 Proof of Corruption Verification (B => D)"
                }
            ]
        }
