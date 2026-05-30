from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from intract.core.models import ContractSignature, ValidationIssue


DEFAULT_VALIDATORS = frozenset({"input_presence", "output_presence", "return_value", "no_forbidden_effect"})


@dataclass
class RuleResult:
    name: str
    score: float
    missing: list[str] = field(default_factory=list)
    violations: list[ValidationIssue] = field(default_factory=list)
    matched: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationContext:
    pass_threshold: float = 0.84
    partial_threshold: float = 0.65


@runtime_checkable
class ValidationRule(Protocol):
    name: str

    def supports(self, validators: frozenset[str]) -> bool:
        ...

    def validate(self, signature: ContractSignature, source: str, context: ValidationContext) -> RuleResult:
        ...


def merge_rule_results(results: list[RuleResult]) -> tuple[list[str], list[ValidationIssue], dict[str, Any], list[float]]:
    missing: list[str] = []
    violations: list[ValidationIssue] = []
    matched: dict[str, Any] = {}
    score_parts: list[float] = []

    for result in results:
        missing.extend(result.missing)
        violations.extend(result.violations)
        matched.update(result.matched)
        score_parts.append(result.score)

    return missing, violations, matched, score_parts
