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


def validate_manifest(path: str | Path) -> ManifestValidationReport:
    manifest_path = Path(path)
    issues: list[ManifestIssue] = []

    if not manifest_path.exists():
        return ManifestValidationReport(
            path=str(manifest_path),
            valid=False,
            issues=[ManifestIssue(path=str(manifest_path), message="Manifest file does not exist.")],
        )

    try:
        data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        return ManifestValidationReport(
            path=str(manifest_path),
            valid=False,
            issues=[ManifestIssue(path=str(manifest_path), message=f"Invalid YAML: {exc}")],
        )

    try:
        from jsonschema import Draft202012Validator

        validator = Draft202012Validator(_load_schema())
        for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
            location = ".".join(str(x) for x in error.path) or "$"
            issues.append(ManifestIssue(path=location, message=error.message))
    except ImportError:
        # Lightweight fallback when jsonschema is not installed.
        contracts = data.get("contracts", [])
        if contracts is not None and not isinstance(contracts, list):
            issues.append(ManifestIssue(path="contracts", message="contracts must be a list"))

        for index, contract in enumerate(contracts or []):
            if not isinstance(contract, dict):
                issues.append(ManifestIssue(path=f"contracts.{index}", message="contract must be an object"))
                continue
            if "scope" not in contract:
                issues.append(ManifestIssue(path=f"contracts.{index}.scope", message="scope is required"))
            if "intent" not in contract:
                issues.append(ManifestIssue(path=f"contracts.{index}.intent", message="intent is required"))

    return ManifestValidationReport(
        path=str(manifest_path),
        valid=not issues,
        issues=issues,
    )
