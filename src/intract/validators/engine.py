from __future__ import annotations

from intract.core.models import ContractSignature, ValidationResult, ValidationStatus

from .base import DEFAULT_VALIDATORS, ValidationContext, merge_rule_results
from .effects import EFFECT_RULES
from .input_output import INPUT_OUTPUT_RULES

RULE_REGISTRY: tuple = INPUT_OUTPUT_RULES + EFFECT_RULES


def validate_contract_against_source(
    signature: ContractSignature,
    source: str,
    *,
    pass_threshold: float = 0.84,
    partial_threshold: float = 0.65,
) -> ValidationResult:
    validators = set(signature.validators) or set(DEFAULT_VALIDATORS)
    context = ValidationContext(pass_threshold=pass_threshold, partial_threshold=partial_threshold)

    rule_results = [
        rule.validate(signature, source, context)
        for rule in RULE_REGISTRY
        if rule.supports(frozenset(validators))
    ]

    missing, violations, matched, score_parts = merge_rule_results(rule_results)
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
