from __future__ import annotations

from pathlib import Path

from intract.core.artifact import ArtifactKind, infer_artifact_kind

from .models import ProjectReport, ValidationResult, ValidationStatus
from .parser import extract_contract_records_from_text
from .signature import build_signatures
from .validation import validate_contract_against_source, validate_required_contracts
from .yaml_manifest import load_manifest_records
from .parsers.toon import load_toon_records

DEFAULT_EXTENSIONS = (".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cs", ".go", ".rs", ".php", ".rb", ".sh", ".sql", ".html", ".css", ".md", ".yaml", ".yml")
EXTRA_ARTIFACT_KINDS = frozenset({ArtifactKind.DOCKERFILE})
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", "dist", "build"}


def load_project_sources(root: Path, *, extensions: tuple[str, ...] = DEFAULT_EXTENSIONS) -> dict[str, str]:
    sources: dict[str, str] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        rel_path = str(path.relative_to(root))
        if path.suffix not in extensions:
            try:
                preview = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if infer_artifact_kind(rel_path, preview) not in EXTRA_ARTIFACT_KINDS:
                continue
        try:
            sources[rel_path] = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
    return sources


def extract_signatures_from_sources(sources: dict[str, str]):
    records = []
    for file_path, source in sources.items():
        records.extend(extract_contract_records_from_text(source, file_path=file_path, default_scope="block"))
    return build_signatures(records)


def validate_sources(sources: dict[str, str], *, manifest_records=None) -> ProjectReport:
    observed_signatures = extract_signatures_from_sources(sources)
    observed_by_file = {file_path: source for file_path, source in sources.items()}
    results: list[ValidationResult] = []

    for signature in observed_signatures:
        source = observed_by_file.get(signature.file_path, "")
        results.append(validate_contract_against_source(signature, source))

    if manifest_records:
        manifest_signatures = build_signatures(manifest_records)
        for required_signature in manifest_signatures:
            satisfied, missing = validate_required_contracts(required_signature, observed_signatures)
            source = observed_by_file.get(required_signature.file_path, "")
            result = validate_contract_against_source(required_signature, source)
            if missing:
                result.status = ValidationStatus.PARTIAL if satisfied else ValidationStatus.FAIL
                result.missing.extend(f"require:{item}" for item in missing)
            result.matched["satisfied_requirements"] = satisfied
            result.evidence["manifest_contract"] = True
            results.append(result)

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
    return ProjectReport(project_path="<sources>", status=status, results=results)


def validate_project(root: Path | str, *, manifest_path: Path | str | None = None) -> ProjectReport:
    project_root = Path(root)
    sources = load_project_sources(project_root)
    manifest_records = []
    
    if manifest_path:
        path = Path(manifest_path)
        if path.suffix == ".toon":
            manifest_records = load_toon_records(path)
        else:
            manifest_records = load_manifest_records(path)
    else:
        # Search candidates
        candidates = [
            ("intract.toon", "toon"),
            ("intent.toon", "toon"),
            ("intract.toon.yaml", "yaml"),
            ("intract.yaml", "yaml"),
            ("intent.yaml", "yaml"),
            (".intract.yaml", "yaml"),
        ]
        for name, kind in candidates:
            path = project_root / name
            if path.exists():
                if kind == "toon":
                    manifest_records = load_toon_records(path)
                else:
                    manifest_records = load_manifest_records(path)
                break
                
    report = validate_sources(sources, manifest_records=manifest_records)
    report.project_path = str(project_root)
    return report
