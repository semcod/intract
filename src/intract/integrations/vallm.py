from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from intract.core.models import ProjectReport, ValidationResult, ValidationStatus


@dataclass(frozen=True)
class MappedIssue:
    rule: str
    message: str
    severity: str
    filename: str | None = None
    line: int | None = None


@dataclass(frozen=True)
class MappedValidationResult:
    score: float
    issues: tuple[MappedIssue, ...]
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "status": self.status,
            "issues": [issue.__dict__ for issue in self.issues],
        }


def map_validation_result(result: ValidationResult) -> MappedIssue:
    if result.status == ValidationStatus.VIOLATION:
        severity = "error"
    elif result.status == ValidationStatus.FAIL:
        severity = "error"
    elif result.status == ValidationStatus.PARTIAL:
        severity = "warning"
    else:
        severity = "info"

    message_parts = [f"{result.contract}: {result.status.value}"]
    message_parts.extend(result.missing)
    message_parts.extend(issue.message for issue in result.violations)
    line = result.lines[0] if result.lines else None

    return MappedIssue(
        rule="intract.contract",
        message="; ".join(message_parts),
        severity=severity,
        filename=result.file_path,
        line=line,
    )


def map_project_report(report: ProjectReport) -> MappedValidationResult:
    issues = tuple(map_validation_result(result) for result in report.results)

    if report.violations:
        score = 0.0
        status = "violation"
    elif report.failed:
        score = 0.4
        status = "fail"
    elif report.partial:
        score = 0.7
        status = "partial"
    elif report.passed and report.results:
        score = 1.0
        status = "pass"
    else:
        score = 1.0
        status = report.status.value

    return MappedValidationResult(score=score, issues=issues, status=status)


def validate_for_vallm(root: str, *, manifest: str | None = None) -> MappedValidationResult:
    from pathlib import Path

    from intract.project import validate_project

    report = validate_project(root, manifest_path=Path(manifest) if manifest else None)
    return map_project_report(report)


def validate_proposal(code: str, *, filename: str | None = None) -> MappedValidationResult:
    """Validate inline @intract contracts in a single code snippet or file body."""
    from intract.core.models import ProjectReport, ValidationStatus
    from intract.core.signatures import build_signatures
    from intract.parsers.inline import extract_contract_records_from_text
    from intract.validators.engine import validate_contract_against_source

    file_path = filename or "<snippet>"
    records = extract_contract_records_from_text(code, file_path=file_path, default_scope="block")
    if not records:
        return MappedValidationResult(score=1.0, issues=(), status="pass")

    results = [
        validate_contract_against_source(signature, code)
        for signature in build_signatures(records)
    ]

    if any(item.status == ValidationStatus.VIOLATION for item in results):
        status = ValidationStatus.VIOLATION
    elif results and all(item.status == ValidationStatus.PASS for item in results):
        status = ValidationStatus.PASS
    elif any(item.status in {ValidationStatus.PASS, ValidationStatus.PARTIAL} for item in results):
        status = ValidationStatus.PARTIAL
    elif results:
        status = ValidationStatus.FAIL
    else:
        status = ValidationStatus.UNKNOWN

    report = ProjectReport(project_path=file_path, status=status, results=results)
    return map_project_report(report)
