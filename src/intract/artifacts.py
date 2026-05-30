from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

from intract.core.models import Contract, ContractRecord, ValidationIssue, ValidationResult, ValidationStatus
from intract.core.signatures import build_signature


@dataclass(frozen=True)
class ArtifactValidationReport:
    path: str
    kind: str
    results: list[ValidationResult]

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "kind": self.kind,
            "results": [result.to_dict() for result in self.results],
        }


def _contract_from_x_intract(data: dict[str, Any], *, default_scope: str, raw: str = "") -> Contract:
    intent = str(data.get("intent", "unknown:unknown"))
    action, obj = intent.split(":", 1) if ":" in intent else (intent, "unknown")
    return Contract(
        action=action,
        object=obj,
        scope=str(data.get("scope", default_scope)),
        priority=int(data.get("priority", 3)),
        domain=str(data.get("domain", "")),
        inputs=tuple(data.get("input", data.get("inputs", [])) or []),
        outputs=tuple(data.get("output", data.get("outputs", [])) or []),
        effects=tuple(data.get("effect", data.get("effects", [])) or []),
        forbidden=tuple(data.get("forbid", data.get("forbidden", [])) or []),
        required=tuple(data.get("require", data.get("requires", [])) or []),
        validators=tuple(data.get("validate", data.get("validators", [])) or []),
        meaning=str(data.get("meaning", "")),
        raw=raw,
    )


def parse_openapi_contracts(path: Path) -> list[ContractRecord]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    records: list[ContractRecord] = []
    paths = data.get("paths", {}) or {}

    for route, methods in paths.items():
        if not isinstance(methods, dict):
            continue
        for method, operation in methods.items():
            if not isinstance(operation, dict):
                continue
            x = operation.get("x-intract")
            if not isinstance(x, dict):
                continue
            contract = _contract_from_x_intract(x, default_scope="endpoint", raw=str(x))
            records.append(
                ContractRecord(
                    contract=contract,
                    file_path=str(path),
                    start_line=1,
                    end_line=1,
                    owner=f"{str(method).upper()} {route}",
                )
            )
    return records


def validate_openapi(path: Path) -> ArtifactValidationReport:
    records = parse_openapi_contracts(path)
    results: list[ValidationResult] = []

    for record in records:
        signature = build_signature(record)
        issues: list[ValidationIssue] = []

        # Method-aware basic check.
        owner = record.owner.lower()
        if owner.startswith("get ") and "write" in signature.effects:
            issues.append(
                ValidationIssue(
                    kind="endpoint_effect_mismatch",
                    message="GET endpoint declares write effect.",
                )
            )
        if "authorize" in signature.required and "security" not in path.read_text(encoding="utf-8").lower():
            issues.append(
                ValidationIssue(
                    kind="missing_security_hint",
                    message="Endpoint requires authorization but no security hint was found in OpenAPI document.",
                    severity="warning",
                )
            )

        results.append(
            ValidationResult(
                contract=signature.key,
                scope=signature.scope,
                status=ValidationStatus.VIOLATION if any(i.severity == "error" for i in issues) else ValidationStatus.PASS,
                score=0.0 if issues else 1.0,
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

    if re.search(r"^FROM\\s+[^\\s:]+:latest\\b", text, re.MULTILINE | re.IGNORECASE):
        issues.append(ValidationIssue(kind="latest_tag", message="Dockerfile uses latest tag."))
    if not re.search(r"^USER\\s+(?!root\\b).+", text, re.MULTILINE | re.IGNORECASE):
        issues.append(ValidationIssue(kind="root_user", message="Dockerfile does not set non-root USER."))
    if re.search(r"\\b(SECRET|TOKEN|PASSWORD|API_KEY)\\s*=", text, re.IGNORECASE):
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

    return ArtifactValidationReport(
        path=str(path),
        kind="github_actions",
        results=[
            ValidationResult(
                contract="validate.ci_pipeline",
                scope="workflow",
                status=ValidationStatus.VIOLATION if any(i.severity == "error" for i in issues) else ValidationStatus.PASS,
                score=0.0 if any(i.severity == "error" for i in issues) else 1.0,
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

    return ArtifactValidationReport(
        path=str(path),
        kind="kubernetes",
        results=[
            ValidationResult(
                contract="deploy.kubernetes_resource",
                scope="deployment",
                status=ValidationStatus.VIOLATION if any(i.severity == "error" for i in issues) else ValidationStatus.PASS,
                score=0.0 if any(i.severity == "error" for i in issues) else 1.0,
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
    if ".github/workflows" in str(p).replace("\\\\", "/"):
        return validate_github_actions(p)
    if p.suffix.lower() in {".yaml", ".yml", ".json"} and "openapi" in text[:500].lower():
        return validate_openapi(p)
    if p.suffix.lower() in {".yaml", ".yml"} and "apiversion:" in text.lower() and "kind:" in text.lower():
        return validate_kubernetes(p)

    return ArtifactValidationReport(path=str(p), kind="unknown", results=[])
