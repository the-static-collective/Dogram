from __future__ import annotations

from typing import Any

from .canonical import sha256_json

SPECIMEN_SCHEMA = "dogram.phaselift.specimen/v0"
TRIAL_SCHEMA = "dogram.phaselift.trial/v0"
RECEIPT_SCHEMA = "dogram.phaselift.receipt/v0"
PENDING_RECEIPT_REF = "phaselift/receipt-under-construction"
REQUIRED_ROLES = ("REPEAT", "TRANSFER", "GENERATE")
REASON_ORDER = (
    "SCHEMA_INVALID",
    "MISSING_TRIAL",
    "DUPLICATE_TRIAL_RECEIPT",
    "CANDIDATE_IDENTITY_CHANGED",
    "TRANSFORMATION_IDENTITY_CHANGED",
    "PROVENANCE_INCOMPLETE",
    "TRANSFER_CONTEXT_NOT_DISTINCT",
    "PLUS_CO_MISSING_VERB",
    "COMPOSITION_ATTRIBUTION_INCOMPLETE",
    "GENERATED_OPERATION_INVALID",
    "DELTA_OMEGA_EMPTY",
    "COMPOSITIONAL_SURPLUS_EMPTY",
    "CIRCULAR_PROMOTION_PROOF",
)
REASON_RANK = {reason: index for index, reason in enumerate(REASON_ORDER)}


def _ordered_reasons(reasons: set[str]) -> list[str]:
    return sorted(reasons, key=lambda reason: (REASON_RANK.get(reason, 10_000), reason))


def _empty_checks() -> dict[str, bool]:
    return {
        "recurs": False,
        "transfers": False,
        "composes": False,
        "generates": False,
        "non_circular": True,
        "provenance_complete": True,
    }


def _decode_trial_roles(
    specimen: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], str | None, str | None]:
    if specimen.get("schema") != SPECIMEN_SCHEMA:
        return {}, "REFUSE", "SCHEMA_INVALID"
    trials = specimen.get("trials")
    if not isinstance(trials, list):
        return {}, "REFUSE", "SCHEMA_INVALID"

    role_map: dict[str, dict[str, Any]] = {}
    seen_trial_ids: set[str] = set()
    seen_receipt_ids: set[str] = set()
    for trial in trials:
        if not isinstance(trial, dict) or trial.get("schema") != TRIAL_SCHEMA:
            return {}, "REFUSE", "SCHEMA_INVALID"
        role = trial.get("role")
        trial_id = trial.get("trial_id")
        receipt_id = trial.get("receipt_id")
        if (
            role not in REQUIRED_ROLES
            or not isinstance(trial_id, str)
            or not trial_id
            or not isinstance(receipt_id, str)
            or not receipt_id
        ):
            return {}, "REFUSE", "SCHEMA_INVALID"
        if role in role_map or trial_id in seen_trial_ids or receipt_id in seen_receipt_ids:
            return {}, "REFUSE", "DUPLICATE_TRIAL_RECEIPT"
        role_map[role] = trial
        seen_trial_ids.add(trial_id)
        seen_receipt_ids.add(receipt_id)

    if any(role not in role_map for role in REQUIRED_ROLES):
        return role_map, "INSUFFICIENT_TO_TEST", "MISSING_TRIAL"
    return role_map, None, None


def _identity_reason(
    specimen: dict[str, Any],
    trials: dict[str, dict[str, Any]],
) -> str | None:
    candidate_id = specimen.get("candidate_id")
    if not isinstance(candidate_id, str) or not candidate_id:
        return "CANDIDATE_IDENTITY_CHANGED"
    candidate_refs = {trial.get("candidate_ref") for trial in trials.values()}
    candidate_digests = {trial.get("candidate_digest") for trial in trials.values()}
    if (
        candidate_refs != {candidate_id}
        or len(candidate_digests) != 1
        or None in candidate_digests
        or "" in candidate_digests
    ):
        return "CANDIDATE_IDENTITY_CHANGED"

    transforms = {
        (trial.get("transformation_id"), trial.get("transformation_version"))
        for trial in trials.values()
    }
    if len(transforms) != 1:
        return "TRANSFORMATION_IDENTITY_CHANGED"
    transform_id, transform_version = next(iter(transforms))
    if (
        not isinstance(transform_id, str)
        or not transform_id
        or type(transform_version) is not int
        or transform_version < 1
    ):
        return "TRANSFORMATION_IDENTITY_CHANGED"
    return None


def _provenance_complete(trials: dict[str, dict[str, Any]]) -> bool:
    for trial in trials.values():
        refs = trial.get("provenance_refs")
        outputs = trial.get("output_refs")
        if (
            not isinstance(refs, list)
            or not refs
            or not all(isinstance(ref, str) and ref for ref in refs)
        ):
            return False
        if (
            not isinstance(outputs, list)
            or not outputs
            or not all(isinstance(ref, str) and ref for ref in outputs)
        ):
            return False
    return True


def _transfer_distinct(
    repeat: dict[str, Any],
    transfer: dict[str, Any],
) -> tuple[bool, list[str]]:
    distinct = transfer.get("distinct_from")
    if not isinstance(distinct, dict) or distinct.get("trial_ref") != repeat.get("trial_id"):
        return False, ["TRANSFER_CONTEXT_NOT_DISTINCT:trial_ref"]
    dimensions = distinct.get("dimensions")
    if (
        not isinstance(dimensions, list)
        or not dimensions
        or not all(isinstance(item, str) and item for item in dimensions)
    ):
        return False, ["TRANSFER_CONTEXT_NOT_DISTINCT:dimensions"]
    left = repeat.get("context_fingerprint")
    right = transfer.get("context_fingerprint")
    if not isinstance(left, dict) or not isinstance(right, dict):
        return False, ["TRANSFER_CONTEXT_NOT_DISTINCT:fingerprint"]
    failures = [
        dimension
        for dimension in dimensions
        if dimension not in left
        or dimension not in right
        or left[dimension] == right[dimension]
    ]
    return not failures, [
        f"TRANSFER_CONTEXT_NOT_DISTINCT:{item}" for item in sorted(failures)
    ]


def _valid_generated_operation(operation: Any) -> bool:
    if not isinstance(operation, dict):
        return False
    if not isinstance(operation.get("operation_id"), str) or not operation["operation_id"]:
        return False
    if type(operation.get("operation_version")) is not int or operation["operation_version"] < 1:
        return False
    input_kinds = operation.get("input_kinds")
    if (
        not isinstance(input_kinds, list)
        or not input_kinds
        or not all(isinstance(item, str) and item for item in input_kinds)
    ):
        return False
    if not isinstance(operation.get("output_kind"), str) or not operation["output_kind"]:
        return False
    derivation_refs = operation.get("derivation_refs")
    if (
        not isinstance(derivation_refs, list)
        or not derivation_refs
        or not all(isinstance(item, str) and item for item in derivation_refs)
    ):
        return False
    return isinstance(operation.get("replay_probe_ref"), str) and bool(
        operation["replay_probe_ref"]
    )


def _grammar_growth(
    generate: dict[str, Any],
) -> tuple[list[str], list[str], list[str], str | None]:
    omega_raw = generate.get("omega_before")
    operations_raw = generate.get("generated_operations")
    if (
        not isinstance(omega_raw, list)
        or not all(isinstance(item, str) and item for item in omega_raw)
    ):
        return [], [], [], "SCHEMA_INVALID"
    if not isinstance(operations_raw, list):
        return [], [], [], "SCHEMA_INVALID"
    if any(not _valid_generated_operation(operation) for operation in operations_raw):
        return [], [], [], "GENERATED_OPERATION_INVALID"
    omega_before = sorted(set(omega_raw))
    generated_ids = sorted({operation["operation_id"] for operation in operations_raw})
    omega_after = sorted(set(omega_before) | set(generated_ids))
    delta_omega = sorted(set(omega_after) - set(omega_before))
    return omega_before, omega_after, delta_omega, None


def _string_list(value: Any) -> list[str] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        return None
    return value


def _composition_check(
    generate: dict[str, Any],
    delta_omega: list[str],
) -> tuple[bool, str | None, list[str]]:
    witnesses = generate.get("composition_witnesses")
    if not isinstance(witnesses, list):
        return False, "SCHEMA_INVALID", []
    inputs_raw = generate.get("input_refs")
    outputs_raw = generate.get("output_refs")
    if _string_list(inputs_raw) is None or _string_list(outputs_raw) is None:
        return False, "SCHEMA_INVALID", []
    inputs = set(inputs_raw)
    outputs = set(outputs_raw)
    delta = set(delta_omega)
    saw_plus_co = False

    for witness in witnesses:
        if not isinstance(witness, dict):
            return False, "SCHEMA_INVALID", []
        if witness.get("phase") != "PLUS_CO":
            continue
        saw_plus_co = True
        if not isinstance(witness.get("verb_id"), str) or not witness["verb_id"]:
            return False, "PLUS_CO_MISSING_VERB", []
        left_ref = witness.get("left_ref")
        right_ref = witness.get("right_ref")
        output_ref = witness.get("output_ref")
        if left_ref not in inputs or right_ref not in inputs or output_ref not in outputs:
            return False, "COMPOSITION_ATTRIBUTION_INCOMPLETE", []

        left_caps = _string_list(witness.get("left_capability_refs"))
        right_caps = _string_list(witness.get("right_capability_refs"))
        output_caps = _string_list(witness.get("output_capability_refs"))
        declared_surplus = _string_list(witness.get("surplus_capability_refs"))
        if any(
            value is None
            for value in (left_caps, right_caps, output_caps, declared_surplus)
        ):
            return False, "COMPOSITION_ATTRIBUTION_INCOMPLETE", []

        assert left_caps is not None and right_caps is not None
        assert output_caps is not None and declared_surplus is not None
        computed = set(output_caps) - (set(left_caps) | set(right_caps))
        declared = set(declared_surplus)
        if declared and declared <= computed and bool(declared & delta):
            return True, None, sorted(declared)

    if saw_plus_co:
        return False, "COMPOSITIONAL_SURPLUS_EMPTY", []
    return False, "COMPOSITIONAL_SURPLUS_EMPTY", []


def _proof_graph(trials: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {
        PENDING_RECEIPT_REF: {trials[role]["trial_id"] for role in REQUIRED_ROLES}
    }
    for trial in trials.values():
        trial_id = trial["trial_id"]
        deps = graph.setdefault(trial_id, set())
        deps.update(trial.get("provenance_refs", []))
        deps.update(trial.get("output_refs", []))
        for witness in trial.get("composition_witnesses", []):
            if not isinstance(witness, dict):
                continue
            output_ref = witness.get("output_ref")
            if isinstance(output_ref, str) and output_ref:
                deps.add(output_ref)
                graph.setdefault(output_ref, set()).update(
                    ref
                    for ref in (witness.get("left_ref"), witness.get("right_ref"))
                    if isinstance(ref, str) and ref
                )
                surplus = witness.get("surplus_capability_refs", [])
                if isinstance(surplus, list):
                    graph[output_ref].update(
                        ref for ref in surplus if isinstance(ref, str) and ref
                    )
        for operation in trial.get("generated_operations", []):
            if not isinstance(operation, dict):
                continue
            operation_id = operation.get("operation_id")
            if not isinstance(operation_id, str) or not operation_id:
                continue
            deps.add(operation_id)
            derivations = operation.get("derivation_refs", [])
            if isinstance(derivations, list):
                graph.setdefault(operation_id, set()).update(
                    ref for ref in derivations if isinstance(ref, str) and ref
                )
            probe = operation.get("replay_probe_ref")
            if isinstance(probe, str) and probe:
                graph[operation_id].add(probe)
    return graph


def _pending_receipt_is_cyclic(graph: dict[str, set[str]]) -> bool:
    seen: set[str] = set()

    def visit(node: str) -> bool:
        if node in seen:
            return False
        seen.add(node)
        for neighbor in sorted(graph.get(node, set())):
            if neighbor == PENDING_RECEIPT_REF:
                return True
            if visit(neighbor):
                return True
        return False

    return any(
        neighbor == PENDING_RECEIPT_REF or visit(neighbor)
        for neighbor in sorted(graph.get(PENDING_RECEIPT_REF, set()))
    )


def _earned_class(checks: dict[str, bool]) -> str:
    if not checks["recurs"]:
        return "REMNANT"
    if not checks["transfers"]:
        return "PATTERN"
    if not (checks["generates"] and checks["composes"]):
        return "TOOL"
    return "OPERATOR_CANDIDATE"


def _build_output(
    specimen: dict[str, Any],
    trials: dict[str, dict[str, Any]],
    checks: dict[str, bool],
    omega_before: list[str],
    omega_after: list[str],
    delta_omega: list[str],
    reasons: set[str],
    residuals: set[str],
    disposition: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate_id = specimen.get("candidate_id")
    if not isinstance(candidate_id, str):
        candidate_id = None
    result = {
        "candidate_id": candidate_id,
        "earned_class": _earned_class(checks),
        "disposition": disposition,
        "checks": {
            "recurs": checks["recurs"],
            "transfers": checks["transfers"],
            "composes": checks["composes"],
            "generates": checks["generates"],
            "non_circular": checks["non_circular"],
            "provenance_complete": checks["provenance_complete"],
        },
        "omega_before": sorted(set(omega_before)),
        "omega_after": sorted(set(omega_after)),
        "delta_omega": sorted(set(delta_omega)),
        "reason_codes": _ordered_reasons(reasons),
        "residuals": sorted(residuals),
        "public_operator_admission": False,
    }
    trial_refs = {
        "repeat": trials.get("REPEAT", {}).get("trial_id"),
        "transfer": trials.get("TRANSFER", {}).get("trial_id"),
        "generate": trials.get("GENERATE", {}).get("trial_id"),
    }
    unsigned_receipt = {
        "schema": RECEIPT_SCHEMA,
        "candidate_id": candidate_id,
        "candidate_version": specimen.get("candidate_version"),
        "input_digest": sha256_json(specimen),
        "trial_refs": trial_refs,
        **result,
    }
    receipt = {
        **unsigned_receipt,
        "receipt_digest": sha256_json(unsigned_receipt),
    }
    return result, receipt


def evaluate_phaselift(
    specimen: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    checks = _empty_checks()
    reasons: set[str] = set()
    residuals: set[str] = set()
    omega_before: list[str] = []
    omega_after: list[str] = []
    delta_omega: list[str] = []

    trials, early_disposition, early_reason = _decode_trial_roles(specimen)
    if early_disposition is not None:
        if early_reason is not None:
            reasons.add(early_reason)
        return _build_output(
            specimen,
            trials,
            checks,
            omega_before,
            omega_after,
            delta_omega,
            reasons,
            residuals,
            early_disposition,
        )

    identity_reason = _identity_reason(specimen, trials)
    if identity_reason is not None:
        reasons.add(identity_reason)
        return _build_output(
            specimen,
            trials,
            checks,
            omega_before,
            omega_after,
            delta_omega,
            reasons,
            residuals,
            "REFUSE",
        )

    if not _provenance_complete(trials):
        checks["provenance_complete"] = False
        reasons.add("PROVENANCE_INCOMPLETE")
        return _build_output(
            specimen,
            trials,
            checks,
            omega_before,
            omega_after,
            delta_omega,
            reasons,
            residuals,
            "REFUSE",
        )

    checks["recurs"] = True
    transfer_ok, transfer_residuals = _transfer_distinct(
        trials["REPEAT"], trials["TRANSFER"]
    )
    checks["transfers"] = transfer_ok
    if not transfer_ok:
        reasons.add("TRANSFER_CONTEXT_NOT_DISTINCT")
        residuals.update(transfer_residuals)

    omega_before, omega_after, delta_omega, growth_reason = _grammar_growth(
        trials["GENERATE"]
    )
    if growth_reason is not None:
        reasons.add(growth_reason)
        return _build_output(
            specimen,
            trials,
            checks,
            omega_before,
            omega_after,
            delta_omega,
            reasons,
            residuals,
            "REFUSE",
        )

    if not delta_omega:
        reasons.add("DELTA_OMEGA_EMPTY")
    else:
        checks["generates"] = True
        composes, composition_reason, surplus = _composition_check(
            trials["GENERATE"], delta_omega
        )
        checks["composes"] = composes
        if composition_reason is not None:
            reasons.add(composition_reason)
            if composition_reason in {
                "COMPOSITION_ATTRIBUTION_INCOMPLETE",
                "SCHEMA_INVALID",
            }:
                return _build_output(
                    specimen,
                    trials,
                    checks,
                    omega_before,
                    omega_after,
                    delta_omega,
                    reasons,
                    residuals,
                    "REFUSE",
                )
            residuals.add(f"{composition_reason}:generate")
        elif surplus:
            residuals.add("COMPOSITIONAL_SURPLUS:" + ",".join(surplus))

    if _pending_receipt_is_cyclic(_proof_graph(trials)):
        checks["non_circular"] = False
        reasons.add("CIRCULAR_PROMOTION_PROOF")
        residuals.add(f"CIRCULAR_PROMOTION_PROOF:{PENDING_RECEIPT_REF}")
        return _build_output(
            specimen,
            trials,
            checks,
            omega_before,
            omega_after,
            delta_omega,
            reasons,
            residuals,
            "REFUSE",
        )

    disposition = (
        "PROMOTE"
        if checks["recurs"]
        and checks["transfers"]
        and checks["generates"]
        and checks["composes"]
        and not reasons
        else "RETAIN"
    )
    return _build_output(
        specimen,
        trials,
        checks,
        omega_before,
        omega_after,
        delta_omega,
        reasons,
        residuals,
        disposition,
    )


__all__ = ["evaluate_phaselift"]
