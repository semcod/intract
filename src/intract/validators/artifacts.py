from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from intract.core.models import ValidationIssue, ValidationResult, ValidationStatus
from intract.core.signatures import build_signature
from intract.parsers.openapi import parse_openapi_contracts


@dataclass(frozen=True)
class ArtifactValidationReport:
    path: str
    kind: str
    results: list[ValidationResult]

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "kind": self.kind,
            "results": [result.to_dict() for result in self.results],
        }


def validate_openapi(path: Path) -> ArtifactValidationReport:
    records = parse_openapi_contracts(path)
    results: list[ValidationResult] = []
    document_text = path.read_text(encoding="utf-8").lower()

    for record in records:
        signature = build_signature(record)
        issues: list[ValidationIssue] = []
        owner = record.owner.lower()

        if owner.startswith("get ") and "write" in signature.effects:
            issues.append(
                ValidationIssue(
                    kind="endpoint_effect_mismatch",
                    message="GET endpoint declares write effect.",
                )
            )
        if "authorize" in signature.required and "security" not in document_text:
            issues.append(
                ValidationIssue(
                    kind="missing_security_hint",
                    message="Endpoint requires authorization but no security hint was found in OpenAPI document.",
                    severity="warning",
                )
            )

        has_errors = any(issue.severity == "error" for issue in issues)
        results.append(
            ValidationResult(
                contract=signature.key,
                scope=signature.scope,
                status=ValidationStatus.VIOLATION if has_errors else ValidationStatus.PASS,
                score=0.0 if has_errors else 1.0,
                file_path=str(path),
                lines=(1, 1),
                violations=issues,
                evidence={"owner": record.owner},
            )
        )

    return ArtifactValidationReport(path=str(path), kind="openapi", results=results)


def validate_dockerfile(path: Path) -> ArtifactValidationReport:
    text = path.read_text(encoding="utf-8")
    issues: list[ValidationIssue] = []

    if re.search(r"^FROM\s+[^\s:]+:latest\b", text, re.MULTILINE | re.IGNORECASE):
        issues.append(ValidationIssue(kind="latest_tag", message="Dockerfile uses latest tag."))
    if not re.search(r"^USER\s+(?!root\b).+", text, re.MULTILINE | re.IGNORECASE):
        issues.append(ValidationIssue(kind="root_user", message="Dockerfile does not set non-root USER."))
    if re.search(r"\b(SECRET|TOKEN|PASSWORD|API_KEY)\s*=", text, re.IGNORECASE):
        issues.append(ValidationIssue(kind="secret_leak", message="Possible secret-like ENV/ARG value in Dockerfile."))

    status = ValidationStatus.VIOLATION if issues else ValidationStatus.PASS
    return ArtifactValidationReport(
        path=str(path),
        kind="dockerfile",
        results=[
            ValidationResult(
                contract="package.container",
                scope="container",
                status=status,
                score=0.0 if issues else 1.0,
                file_path=str(path),
                lines=(1, 1),
                violations=issues,
            )
        ],
    )


def validate_github_actions(path: Path) -> ArtifactValidationReport:
    text = path.read_text(encoding="utf-8")
    issues: list[ValidationIssue] = []
    lowered = text.lower()

    if "pull_request" in lowered and any(x in lowered for x in ["twine upload", "npm publish", "docker push"]):
        issues.append(
            ValidationIssue(
                kind="forbidden_publish",
                message="Pull request workflow appears to publish artifacts.",
            )
        )
    if "permissions:" not in lowered:
        issues.append(
            ValidationIssue(
                kind="missing_permissions",
                message="Workflow does not define permissions block.",
                severity="warning",
            )
        )

    has_errors = any(issue.severity == "error" for issue in issues)
    return ArtifactValidationReport(
        path=str(path),
        kind="github_actions",
        results=[
            ValidationResult(
                contract="validate.ci_pipeline",
                scope="workflow",
                status=ValidationStatus.VIOLATION if has_errors else ValidationStatus.PASS,
                score=0.0 if has_errors else 1.0,
                file_path=str(path),
                lines=(1, 1),
                violations=issues,
            )
        ],
    )


def validate_kubernetes(path: Path) -> ArtifactValidationReport:
    text = path.read_text(encoding="utf-8")
    issues: list[ValidationIssue] = []
    lowered = text.lower()

    if ":latest" in lowered:
        issues.append(ValidationIssue(kind="latest_image", message="Kubernetes manifest uses image:latest."))
    if "resources:" not in lowered:
        issues.append(ValidationIssue(kind="missing_resources", message="No resources block found.", severity="warning"))
    if "readinessprobe:" not in lowered and "livenessprobe:" not in lowered:
        issues.append(ValidationIssue(kind="missing_probe", message="No readiness/liveness probe found.", severity="warning"))

    has_errors = any(issue.severity == "error" for issue in issues)
    return ArtifactValidationReport(
        path=str(path),
        kind="kubernetes",
        results=[
            ValidationResult(
                contract="deploy.kubernetes_resource",
                scope="deployment",
                status=ValidationStatus.VIOLATION if has_errors else ValidationStatus.PASS,
                score=0.0 if has_errors else 1.0,
                file_path=str(path),
                lines=(1, 1),
                violations=issues,
            )
        ],
    )


def validate_artifact(path: str | Path) -> ArtifactValidationReport:
    p = Path(path)
    name = p.name.lower()
    text = p.read_text(encoding="utf-8")

    if name == "dockerfile" or name.startswith("dockerfile."):
        return validate_dockerfile(p)
    if ".github/workflows" in str(p).replace("\\", "/"):
        return validate_github_actions(p)
    if p.suffix.lower() in {".yaml", ".yml", ".json"} and "openapi" in text[:500].lower():
        return validate_openapi(p)
    if p.suffix.lower() in {".yaml", ".yml"} and "apiversion:" in text.lower() and "kind:" in text.lower():
        return validate_kubernetes(p)

    return ArtifactValidationReport(path=str(p), kind="unknown", results=[])
