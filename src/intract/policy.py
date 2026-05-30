from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PolicyDecision:
    should_fail: bool
    reasons: list[str]
    warnings: list[str]


def decide_policy(
    report: Any,
    *,
    fail_on: list[str] | None = None,
    warn_on: list[str] | None = None,
) -> PolicyDecision:
    fail_on = fail_on or ["violation", "fail", "invalid_manifest"]
    warn_on = warn_on or ["partial", "unknown"]

    reasons: list[str] = []
    warnings: list[str] = []

    for result in getattr(report, "results", []) or []:
        status = getattr(getattr(result, "status", ""), "value", str(getattr(result, "status", "")))
        contract = getattr(result, "contract", "unknown.contract")
        file_path = getattr(result, "file_path", "")

        if status in fail_on:
            reasons.append(f"{status}: {contract} {file_path}".strip())
        elif status in warn_on:
            warnings.append(f"{status}: {contract} {file_path}".strip())

    return PolicyDecision(should_fail=bool(reasons), reasons=reasons, warnings=warnings)
