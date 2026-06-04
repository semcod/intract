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


def _result_status(result: Any) -> str:
    raw_status = getattr(result, "status", "")
    return getattr(raw_status, "value", str(raw_status))


def _result_policy_line(result: Any, status: str) -> str:
    contract = getattr(result, "contract", "unknown.contract")
    file_path = getattr(result, "file_path", "")
    return f"{status}: {contract} {file_path}".strip()


def _collect_result_policy(
    report: Any,
    *,
    fail_on: list[str],
    warn_on: list[str],
) -> tuple[list[str], list[str]]:
    reasons: list[str] = []
    warnings: list[str] = []

    for result in getattr(report, "results", []) or []:
        status = _result_status(result)
        line = _result_policy_line(result, status)
        if status in fail_on:
            reasons.append(line)
        elif status in warn_on:
            warnings.append(line)

    return reasons, warnings


def _invalid_manifest_reasons(manifest_path: str | Path) -> list[str]:
    from .manifest_schema import validate_manifest

    manifest_report = validate_manifest(manifest_path)
    if manifest_report.valid:
        return []
    return [
        f"invalid_manifest: {issue.path}: {issue.message}"
        for issue in manifest_report.issues
    ]


def _missing_required_p1_reasons(graph: Any | None, manifest_path: str | Path | None) -> list[str]:
    if graph is None or manifest_path is None:
        return []
    manifest = Path(manifest_path)
    if not manifest.exists():
        return []
    return _p1_missing_reasons(graph, manifest)


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

    reasons, warnings = _collect_result_policy(report, fail_on=fail_on, warn_on=warn_on)

    if "missing_required_p1" in fail_on:
        reasons.extend(_missing_required_p1_reasons(graph, manifest_path))

    if "invalid_manifest" in fail_on and manifest_path is not None:
        reasons.extend(_invalid_manifest_reasons(manifest_path))

    return PolicyDecision(should_fail=bool(reasons), reasons=reasons, warnings=warnings)
