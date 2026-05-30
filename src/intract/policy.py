from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PolicyDecision:
    should_fail: bool
    reasons: list[str]
    warnings: list[str]


def _p1_missing_reasons(graph: Any, manifest_path: Path) -> list[str]:
    from .normalizer import normalize_requirement
    from .signature import build_signatures
    from .yaml_manifest import load_manifest_records

    if not graph or not getattr(graph, "missing", None):
        return []

    missing_set = set(graph.missing)
    reasons: list[str] = []
    for signature in build_signatures(load_manifest_records(manifest_path)):
        if signature.priority != 1:
            continue
        for requirement in signature.required:
            normalized = normalize_requirement(requirement)
            if normalized in missing_set:
                reasons.append(f"missing_required_p1: {normalized} required by {signature.key}")
    return reasons


def decide_policy(
    report: Any,
    *,
    fail_on: list[str] | None = None,
    warn_on: list[str] | None = None,
    graph: Any | None = None,
    manifest_path: str | Path | None = None,
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

    if "missing_required_p1" in fail_on and graph is not None and manifest_path is not None:
        manifest = Path(manifest_path)
        if manifest.exists():
            reasons.extend(_p1_missing_reasons(graph, manifest))

    if "invalid_manifest" in fail_on and manifest_path is not None:
        from .manifest_schema import validate_manifest

        manifest_report = validate_manifest(manifest_path)
        if not manifest_report.valid:
            for issue in manifest_report.issues:
                reasons.append(f"invalid_manifest: {issue.path}: {issue.message}")

    return PolicyDecision(should_fail=bool(reasons), reasons=reasons, warnings=warnings)
