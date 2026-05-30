from __future__ import annotations

from importlib.metadata import entry_points

from .base import DEFAULT_VALIDATORS, RuleResult, ValidationContext, ValidationRule
from .effects import EFFECT_RULES
from .input_output import INPUT_OUTPUT_RULES

_BUILTIN_RULES: tuple[ValidationRule, ...] = INPUT_OUTPUT_RULES + EFFECT_RULES


def _discover_entry_point_rules() -> list[ValidationRule]:
    rules: list[ValidationRule] = []
    try:
        eps = entry_points(group="intract.rules")
    except TypeError:
        eps = entry_points().get("intract.rules", [])
    for ep in eps:
        rule = ep.load()()
        if hasattr(rule, "validate") and hasattr(rule, "name"):
            rules.append(rule)
    return rules


class RuleRegistry:
    """Registry of contract validation rules with optional plugin discovery."""

    def __init__(self, rules: tuple[ValidationRule, ...] | None = None):
        self._rules: list[ValidationRule] = list(rules if rules is not None else _BUILTIN_RULES)

    def register(self, rule: ValidationRule) -> None:
        if rule.name not in {item.name for item in self._rules}:
            self._rules.append(rule)

    def rules(self) -> tuple[ValidationRule, ...]:
        return tuple(self._rules)

    def run(
        self,
        signature,
        source: str,
        context: ValidationContext,
        validators: frozenset[str] | None = None,
    ) -> list[RuleResult]:
        active = validators or (set(signature.validators) or set(DEFAULT_VALIDATORS))
        active_frozen = frozenset(active)
        return [
            rule.validate(signature, source, context)
            for rule in self._rules
            if rule.supports(active_frozen)
        ]

    @staticmethod
    def rule_status(result: RuleResult, context: ValidationContext) -> str:
        if result.violations:
            return "fail"
        if result.missing and result.score < context.pass_threshold:
            return "fail"
        if result.missing:
            return "partial"
        if result.score >= context.pass_threshold:
            return "pass"
        if result.score >= context.partial_threshold:
            return "partial"
        return "fail"

    def summarize(self, results: list[RuleResult], context: ValidationContext) -> dict[str, str]:
        return {result.name: self.rule_status(result, context) for result in results}


_default_registry: RuleRegistry | None = None


def get_rule_registry(*, discover: bool = True) -> RuleRegistry:
    global _default_registry
    if _default_registry is None:
        rules: list[ValidationRule] = list(_BUILTIN_RULES)
        if discover:
            seen = {rule.name for rule in rules}
            for rule in _discover_entry_point_rules():
                if rule.name not in seen:
                    rules.append(rule)
                    seen.add(rule.name)
        _default_registry = RuleRegistry(tuple(rules))
    return _default_registry
