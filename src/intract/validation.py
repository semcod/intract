from __future__ import annotations

import re

from .effects import detect_effects
from .models import ContractSignature, ValidationIssue, ValidationResult, ValidationStatus
from .normalizer import normalize_label

DEFAULT_VALIDATORS = {"input_presence", "output_presence", "return_value", "no_forbidden_effect"}


def contains_token_like(source: str, token: str) -> bool:
    normalized_source = normalize_label(source)
    normalized_token = normalize_label(token)
    if not normalized_token:
        return True
    if normalized_token in normalized_source:
        return True
    parts = [part for part in normalized_token.split("_") if part]
    return bool(parts) and all(part in normalized_source for part in parts)


def has_return_value(source: str) -> bool:
    return bool(re.search(r"\breturn\b", source) or re.search(r"=>", source) or re.search(r"\byield\b", source))


def validate_contract_against_source(
    signature: ContractSignature,
    source: str,
    *,
    pass_threshold: float = 0.84,
    partial_threshold: float = 0.65,
) -> ValidationResult:
    validators = set(signature.validators) or DEFAULT_VALIDATORS
    missing: list[str] = []
    violations: list[ValidationIssue] = []
    matched: dict[str, object] = {}
    score_parts: list[float] = []

    if "input_presence" in validators:
        found = [item for item in signature.inputs if contains_token_like(source, item)]
        missing_inputs = sorted(signature.inputs - set(found))
        matched["inputs_found"] = found
        if missing_inputs:
            missing.extend(f"input:{item}" for item in missing_inputs)
        score_parts.append(len(found) / max(1, len(signature.inputs)) if signature.inputs else 1.0)

    if "output_presence" in validators:
        found = [item for item in signature.outputs if contains_token_like(source, item)]
        missing_outputs = sorted(signature.outputs - set(found))
        matched["outputs_found"] = found
        if missing_outputs:
            missing.extend(f"output:{item}" for item in missing_outputs)
        score_parts.append(len(found) / max(1, len(signature.outputs)) if signature.outputs else 1.0)

    if "return_value" in validators:
        has_return = has_return_value(source)
        matched["has_return"] = has_return
        if not has_return:
            missing.append("return_value")
        score_parts.append(1.0 if has_return else 0.0)

    observed_effects = detect_effects(source)
    matched["observed_effects"] = sorted(observed_effects)

    if "no_forbidden_effect" in validators:
        forbidden_hits = sorted(signature.forbidden & observed_effects)
        for item in forbidden_hits:
            violations.append(
                ValidationIssue(kind="forbidden_effect", message=f"Declared forbid:{item}, but effect '{item}' was detected.")
            )
        score_parts.append(1.0 if not forbidden_hits else 0.0)

    score = sum(score_parts) / max(1, len(score_parts))
    if violations:
        status = ValidationStatus.VIOLATION
    elif score >= pass_threshold and not missing:
        status = ValidationStatus.PASS
    elif score >= partial_threshold or missing:
        status = ValidationStatus.PARTIAL
    else:
        status = ValidationStatus.FAIL

    return ValidationResult(
        contract=signature.key,
        scope=signature.scope,
        status=status,
        score=round(score, 4),
        file_path=signature.file_path,
        lines=(signature.start_line, signature.end_line),
        matched=matched,
        missing=missing,
        violations=violations,
        evidence={"meaning": signature.meaning, "validators": sorted(validators)},
    )


def validate_required_contracts(required_signature: ContractSignature, observed_signatures: list[ContractSignature]) -> tuple[list[str], list[str]]:
    observed_keys = {item.key for item in observed_signatures}
    satisfied = sorted(item for item in required_signature.required if item in observed_keys)
    missing = sorted(item for item in required_signature.required if item not in observed_keys)
    return satisfied, missing
