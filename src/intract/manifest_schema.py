from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ManifestIssue:
    path: str
    message: str
    severity: str = "error"


@dataclass(frozen=True)
class ManifestValidationReport:
    path: str
    valid: bool
    issues: list[ManifestIssue]

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "valid": self.valid,
            "issues": [asdict(issue) for issue in self.issues],
        }


def _load_schema() -> dict[str, Any]:
    schema_path = Path(__file__).resolve().parents[2] / "schemas" / "intract.schema.json"
    if schema_path.exists():
        import json

        return json.loads(schema_path.read_text(encoding="utf-8"))

    return {
        "type": "object",
        "properties": {
            "contracts": {"type": "array"},
            "files": {"type": "object"},
            "artifacts": {"type": "object"},
        },
    }


def _manifest_report(path: Path, issues: list[ManifestIssue]) -> ManifestValidationReport:
    return ManifestValidationReport(path=str(path), valid=not issues, issues=issues)


def _invalid_manifest_report(path: Path, message: str) -> ManifestValidationReport:
    return _manifest_report(path, [ManifestIssue(path=str(path), message=message)])


def _load_manifest_data(path: Path) -> tuple[Any, ManifestValidationReport | None]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}, None
    except Exception as exc:
        return None, _invalid_manifest_report(path, f"Invalid YAML: {exc}")


def _jsonschema_issues(data: Any) -> list[ManifestIssue] | None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return None

    validator = Draft202012Validator(_load_schema())
    return [
        ManifestIssue(path=".".join(str(x) for x in error.path) or "$", message=error.message)
        for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    ]


def _fallback_issues(data: Any) -> list[ManifestIssue]:
    issues: list[ManifestIssue] = []
    if not isinstance(data, dict):
        return [ManifestIssue(path="$", message="manifest must be an object")]

    contracts = data.get("contracts", [])
    if contracts is not None and not isinstance(contracts, list):
        issues.append(ManifestIssue(path="contracts", message="contracts must be a list"))
        return issues

    for index, contract in enumerate(contracts or []):
        if not isinstance(contract, dict):
            issues.append(
                ManifestIssue(path=f"contracts.{index}", message="contract must be an object")
            )
            continue
        if "scope" not in contract:
            issues.append(
                ManifestIssue(path=f"contracts.{index}.scope", message="scope is required")
            )
        if "intent" not in contract:
            issues.append(
                ManifestIssue(path=f"contracts.{index}.intent", message="intent is required")
            )
    return issues


def validate_manifest(path: str | Path) -> ManifestValidationReport:
    manifest_path = Path(path)
    if not manifest_path.exists():
        return _invalid_manifest_report(manifest_path, "Manifest file does not exist.")

    data, error_report = _load_manifest_data(manifest_path)
    if error_report is not None:
        return error_report

    issues = _jsonschema_issues(data)
    if issues is None:
        issues = _fallback_issues(data)

    return _manifest_report(manifest_path, issues)
