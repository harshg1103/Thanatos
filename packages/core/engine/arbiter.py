import time
import uuid
import hashlib
import json
from typing import Dict, List, Optional, Tuple, Any
import z3

from packages.core.schemas.proof import SMTFormula, Z3ProofCertificate, JSONLDProof
from packages.core.schemas.belief import BeliefNode, BeliefEdge, BeliefGraph


class ArbiterZ3Engine:
    """
    ARBITER: High-Assurance Formal Verification & SMT Proof Oracle.
    Translates multi-agent belief DAGs into First-Order SMT-LIB2 logic formulas
    (Quantifier-Free Uninterpreted Functions & Linear Real Arithmetic).
    Executes Microsoft Z3 to formally verify entailment (B |= D), extract minimal Unsat Cores,
    and generate cryptographic Merkle Proof certificates.
    """

    def __init__(self, solver_timeout_ms: int = 5000, logic_theory: str = "QF_UF"):
        self.solver_timeout_ms = solver_timeout_ms
        self.logic_theory = logic_theory

    def sanitize_var_name(self, name: str) -> str:
        """Sanitizes node IDs or propositions into valid SMT-LIB variable identifiers."""
        clean = "".join(c if c.isalnum() else "_" for c in name)
        if not clean or clean[0].isdigit():
            clean = "v_" + clean
        return clean[:32]

    def compute_merkle_root(self, leaves: List[str]) -> str:
        """Computes a cryptographic Merkle root from a list of proof strings."""
        if not leaves:
            return hashlib.sha256(b"empty_proof").hexdigest()
        hashes = [hashlib.sha256(leaf.encode('utf-8')).hexdigest() for leaf in leaves]
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])
            new_level = []
            for i in range(0, len(hashes), 2):
                combined = (hashes[i] + hashes[i+1]).encode('utf-8')
                new_level.append(hashlib.sha256(combined).hexdigest())
            hashes = new_level
        return hashes[0]

    def encode_belief_graph_to_smt(
        self,
        belief_graph: BeliefGraph,
        injected_node_id: str,
        corrupted_decision_id: str,
        numeric_constraints: Optional[Dict[str, Tuple[str, float]]] = None
    ) -> SMTFormula:
        """
        Translates a BeliefGraph into standards-compliant SMT-LIB2 format.
        Encodes belief propositions as Boolean predicates, causal inferences as implications,
        and records tracked assertion labels for minimal Unsat Core extraction.
        """
        variables: List[str] = []
        assertions: List[str] = []
        tracked_assertions: Dict[str, str] = {}
        var_map: Dict[str, str] = {}

        # 1. Declare Boolean variables for all belief nodes
        for node in belief_graph.nodes:
            v_name = self.sanitize_var_name(node.node_id)
            var_map[node.node_id] = v_name
            variables.append(v_name)

        # 2. Encode causal edges as logical implications (source => target)
        for idx, edge in enumerate(belief_graph.edges):
            src_var = var_map.get(edge.source_id)
            tgt_var = var_map.get(edge.target_id)
            if src_var and tgt_var:
                assertion_label = f"axiom_edge_{idx}_{src_var}_to_{tgt_var}"
                if edge.dependency_type in ("implies", "supports"):
                    expr = f"(=> {src_var} {tgt_var})"
                elif edge.dependency_type == "contradicts":
                    expr = f"(=> {src_var} (not {tgt_var}))"
                else:
                    expr = f"(=> {src_var} {tgt_var})"

                assertions.append(expr)
                tracked_assertions[assertion_label] = expr

        # 3. Assert the injected belief condition
        inj_var = var_map.get(injected_node_id, self.sanitize_var_name(injected_node_id))
        if inj_var not in variables:
            variables.append(inj_var)

        inj_label = f"injected_premise_{inj_var}"
        assertions.append(inj_var)
        tracked_assertions[inj_label] = inj_var

        # 4. Format SMT-LIB v2 string with theory header
        smt_lines = [
            f"; THANATOS ARBITER SMT-LIB v2 Formal Verification Model",
            f"; Target: Proof of Belief Corruption Entailment ({inj_var} |= {var_map.get(corrupted_decision_id, 'd_out')})",
            f"(set-logic {self.logic_theory})",
            f"(set-option :produce-unsat-cores true)",
            f"(set-option :produce-models true)"
        ]

        unique_vars = sorted(list(set(variables)))
        for v in unique_vars:
            smt_lines.append(f"(declare-const {v} Bool)")

        for label, expr in tracked_assertions.items():
            smt_lines.append(f"(assert (! {expr} :named {label}))")

        # Refutation query for decision variable
        dec_var = var_map.get(corrupted_decision_id, self.sanitize_var_name(corrupted_decision_id))
        if dec_var not in variables:
            variables.append(dec_var)
            smt_lines.append(f"(declare-const {dec_var} Bool)")
        smt_lines.append(f"(assert (! (not {dec_var}) :named refutation_not_{dec_var}))")

        smt_lines.append("(check-sat)")
        smt_lines.append("(get-unsat-core)")

        smtlib_code = "\n".join(smt_lines)
        formula_id = f"smt_{uuid.uuid4().hex[:8]}"

        return SMTFormula(
            formula_id=formula_id,
            smtlib_code=smtlib_code,
            variables=unique_vars,
            assertions=assertions,
            logic_theory=self.logic_theory,
            tracked_assertions=tracked_assertions
        )

    def verify_causality_with_z3(
        self,
        belief_graph: BeliefGraph,
        injected_node_id: str,
        corrupted_decision_id: str
    ) -> Z3ProofCertificate:
        """
        Executes Microsoft Z3 formal SMT verification.
        Tests entailment via refutation: (Premises & InjectedBelief & ~CorruptedDecision) == UNSAT.
        Extracts minimal Unsat Core and resolution deduction steps.
        """
        start_time = time.perf_counter()
        smt_formula = self.encode_belief_graph_to_smt(
            belief_graph, injected_node_id, corrupted_decision_id
        )

        solver = z3.Solver()
        solver.set("timeout", self.solver_timeout_ms)
        solver.set("unsat_core", True)

        z3_vars: Dict[str, z3.BoolRef] = {}
        for var_name in smt_formula.variables:
            z3_vars[var_name] = z3.Bool(var_name)

        # Tracked assertions map
        tracked_map: Dict[z3.BoolRef, str] = {}

        # 1. Add background causal edges with tracking
        for idx, edge in enumerate(belief_graph.edges):
            src_name = self.sanitize_var_name(edge.source_id)
            tgt_name = self.sanitize_var_name(edge.target_id)
            if src_name in z3_vars and tgt_name in z3_vars:
                src_b = z3_vars[src_name]
                tgt_b = z3_vars[tgt_name]
                label_name = f"edge_{idx}_{src_name}_to_{tgt_name}"
                tracker = z3.Bool(label_name)
                tracked_map[tracker] = label_name

                if edge.dependency_type in ("implies", "supports"):
                    solver.assert_and_track(z3.Implies(src_b, tgt_b), tracker)
                elif edge.dependency_type == "contradicts":
                    solver.assert_and_track(z3.Implies(src_b, z3.Not(tgt_b)), tracker)

        # 2. Add injected belief with tracking
        inj_name = self.sanitize_var_name(injected_node_id)
        dec_name = self.sanitize_var_name(corrupted_decision_id)

        inj_var = z3_vars.get(inj_name, z3.Bool(inj_name))
        dec_var = z3_vars.get(dec_name, z3.Bool(dec_name))

        inj_tracker = z3.Bool(f"track_injected_{inj_name}")
        tracked_map[inj_tracker] = f"track_injected_{inj_name}"
        solver.assert_and_track(inj_var, inj_tracker)

        # 3. Add negation of corrupted decision with tracking
        refutation_tracker = z3.Bool(f"track_refutation_{dec_name}")
        tracked_map[refutation_tracker] = f"track_refutation_{dec_name}"
        solver.assert_and_track(z3.Not(dec_var), refutation_tracker)

        # 4. Check satisfiability
        sat_result = solver.check()
        exec_time_ms = round((time.perf_counter() - start_time) * 1000, 3)

        unsat_core_labels: List[str] = []
        model_counterexample: Optional[Dict[str, Any]] = None
        deduction_steps: List[str] = []

        is_provably_causal = (sat_result == z3.unsat)

        if is_provably_causal:
            # Extract minimal Unsat Core
            core = solver.unsat_core()
            unsat_core_labels = [str(elem) for elem in core]

            # Construct deductive resolution steps
            deduction_steps.append(f"Step 0: Assume injected false premise [{inj_name}] = TRUE.")
            for step_idx, elem in enumerate(core, 1):
                label_str = str(elem)
                if label_str.startswith("edge_"):
                    parts = label_str.split("_")
                    if len(parts) >= 4:
                        deduction_steps.append(f"Step {step_idx}: By causal handoff ({parts[2]} => {parts[-1]}), propagate premise downstream.")
            deduction_steps.append(f"Step Final: Contradiction established with negation (not {dec_name}) -> [{dec_name}] = TRUE is mathematically entailed (Q.E.D.).")
        else:
            # SAT or UNKNOWN: extract counterexample assignment
            try:
                model = solver.model()
                model_counterexample = {str(d): str(model[d]) for d in model.decls()}
            except Exception:
                model_counterexample = {"note": "No counterexample model could be extracted"}

        # Merkle root calculation for proof integrity
        proof_leaves = [
            smt_formula.smtlib_code,
            str(is_provably_causal),
            ",".join(unsat_core_labels),
            str(exec_time_ms)
        ]
        merkle_root = self.compute_merkle_root(proof_leaves)

        cert_id = f"cert_z3_{uuid.uuid4().hex[:8]}"
        proof_depth = len(unsat_core_labels) if unsat_core_labels else (len(belief_graph.edges) + 1)

        return Z3ProofCertificate(
            certificate_id=cert_id,
            injected_belief_id=injected_node_id,
            corrupted_decision_id=corrupted_decision_id,
            is_provably_causal=is_provably_causal,
            smt_formula=smt_formula,
            proof_tree_depth=proof_depth,
            solver_execution_time_ms=exec_time_ms,
            unsat_core=unsat_core_labels,
            model_counterexample=model_counterexample,
            deduction_steps=deduction_steps,
            merkle_root=merkle_root
        )

    def export_jsonld_certificate(
        self,
        certificate: Z3ProofCertificate,
        injected_premise: str,
        corrupted_decision_text: str
    ) -> JSONLDProof:
        """
        Exports a W3C-compliant JSON-LD security proof certificate
        with Merkle root and cryptographic SHA-256 integrity hash.
        """
        proof_payload = {
            "certificate_id": certificate.certificate_id,
            "injected_node_id": certificate.injected_belief_id,
            "corrupted_decision_id": certificate.corrupted_decision_id,
            "logic_theory": certificate.smt_formula.logic_theory,
            "solver": "Microsoft Z3 Theorem Prover v4.12+",
            "solver_time_ms": certificate.solver_execution_time_ms,
            "proof_depth": certificate.proof_tree_depth,
            "unsat_core": certificate.unsat_core,
            "merkle_root": certificate.merkle_root,
            "deduction_steps": certificate.deduction_steps,
            "timestamp": certificate.timestamp.isoformat()
        }

        content_hash = hashlib.sha256(json.dumps(proof_payload, sort_keys=True).encode('utf-8')).hexdigest()

        return JSONLDProof(
            context="https://w3id.org/security/v1",
            id=f"urn:thanatos:proof:{certificate.certificate_id}",
            type="ProofOfCorruptionCertificate",
            injectedBelief=injected_premise,
            corruptedDecision=corrupted_decision_text,
            causalityVerified=certificate.is_provably_causal,
            proofDetails={
                **proof_payload,
                "sha256_digest": content_hash,
                "verification_status": "FORMALLY_VERIFIED" if certificate.is_provably_causal else "INCONCLUSIVE"
            }
        )
