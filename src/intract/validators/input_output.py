from __future__ import annotations

import re

from intract.core.normalizer import normalize_label

from .base import RuleResult, ValidationContext, ValidationRule


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


class InputPresenceRule:
    name = "input_presence"

    def supports(self, validators: frozenset[str]) -> bool:
        return self.name in validators

    def validate(self, signature, source, context: ValidationContext) -> RuleResult:
        found = [item for item in signature.inputs if contains_token_like(source, item)]
        missing_inputs = sorted(signature.inputs - set(found))
        missing = [f"input:{item}" for item in missing_inputs]
        score = len(found) / max(1, len(signature.inputs)) if signature.inputs else 1.0
        return RuleResult(name=self.name, score=score, missing=missing, matched={"inputs_found": found})


class OutputPresenceRule:
    name = "output_presence"

    def supports(self, validators: frozenset[str]) -> bool:
        return self.name in validators

    def validate(self, signature, source, context: ValidationContext) -> RuleResult:
        found = [item for item in signature.outputs if contains_token_like(source, item)]
        missing_outputs = sorted(signature.outputs - set(found))
        missing = [f"output:{item}" for item in missing_outputs]
        score = len(found) / max(1, len(signature.outputs)) if signature.outputs else 1.0
        return RuleResult(name=self.name, score=score, missing=missing, matched={"outputs_found": found})


class ReturnValueRule:
    name = "return_value"

    def supports(self, validators: frozenset[str]) -> bool:
        return self.name in validators

    def validate(self, signature, source, context: ValidationContext) -> RuleResult:
        has_return = has_return_value(source)
        missing = [] if has_return else ["return_value"]
        return RuleResult(
            name=self.name,
            score=1.0 if has_return else 0.0,
            missing=missing,
            matched={"has_return": has_return},
        )


INPUT_OUTPUT_RULES: tuple[ValidationRule, ...] = (
    InputPresenceRule(),
    OutputPresenceRule(),
    ReturnValueRule(),
)
