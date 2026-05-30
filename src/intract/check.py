from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .git import changed_files, paths_from_changes, staged_files, staged_hunks
from .project import validate_sources
from .yaml_manifest import load_manifest_records


@dataclass(frozen=True)
class ChangedHunk:
    file_path: str
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    header: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


HUNK_RE = re.compile(
    r"^@@\s+-(?P<old_start>\d+)(?:,(?P<old_count>\d+))?\s+"
    r"\+(?P<new_start>\d+)(?:,(?P<new_count>\d+))?\s+@@(?P<header>.*)$"
)


def parse_unified_diff_hunks(diff_text: str) -> list[ChangedHunk]:
    hunks: list[ChangedHunk] = []
    current_file = ""

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[len("+++ b/"):]
            continue

        match = HUNK_RE.match(line)
        if not match:
            continue

        hunks.append(
            ChangedHunk(
                file_path=current_file,
                old_start=int(match.group("old_start")),
                old_count=int(match.group("old_count") or "1"),
                new_start=int(match.group("new_start")),
                new_count=int(match.group("new_count") or "1"),
                header=match.group("header").strip(),
            )
        )

    return hunks


def load_selected_sources(root: str | Path, files: list[str]) -> dict[str, str]:
    root = Path(root)
    sources: dict[str, str] = {}

    for file_path in files:
        path = root / file_path
        if not path.exists() or not path.is_file():
            continue
        try:
            sources[file_path] = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

    return sources


MANIFEST_NAMES = {"intent.yaml", "intract.yaml", ".intract.yaml"}


def _manifest_changed(files: list[str]) -> bool:
    return any(Path(file_path).name in MANIFEST_NAMES for file_path in files)


def changed_lines_by_file(hunks: list[ChangedHunk]) -> dict[str, set[int]]:
    result: dict[str, set[int]] = {}
    for hunk in hunks:
        lines = result.setdefault(hunk.file_path, set())
        count = hunk.new_count or 1
        for line in range(hunk.new_start, hunk.new_start + count):
            lines.add(line)
    return result


def block_extent(source: str, start_line: int) -> tuple[int, int]:
    """Approximate block extent after an @intract comment (function/class body)."""
    lines = source.splitlines()
    if start_line < 1 or start_line > len(lines):
        return start_line, start_line

    end = start_line
    in_block = False

    for index in range(start_line + 1, len(lines) + 1):
        line = lines[index - 1]
        stripped = line.strip()

        if not in_block:
            if stripped.startswith(("def ", "class ", "async def ")):
                in_block = True
                end = index
                continue
            if (
                stripped.startswith("#")
                or not stripped
                or stripped.startswith(("import ", "from "))
            ):
                end = index
                continue
            break

        if not stripped:
            end = index
            continue
        if line[0].isspace():
            end = index
            continue
        if stripped.startswith(("def ", "class ", "async def ")) or "@intract" in line:
            break
        break

    return start_line, end


def signature_touched(signature, changed_lines: set[int], source: str) -> bool:
    if signature.start_line in changed_lines:
        return True
    start, end = block_extent(source, signature.start_line)
    return bool(changed_lines.intersection(range(start, end + 1)))


def validate_sources_for_hunks(
    root: str | Path,
    files: list[str],
    hunks: list[ChangedHunk],
    *,
    manifest: str | Path | None = None,
):
    from .models import ProjectReport, ValidationStatus
    from .parser import extract_contract_records_from_text
    from .signature import build_signatures
    from .validation import validate_contract_against_source

    root = Path(root)
    sources = load_selected_sources(root, files)
    changed = changed_lines_by_file(hunks)

    all_signatures = []
    for file_path, source in sources.items():
        records = extract_contract_records_from_text(source, file_path=file_path, default_scope="block")
        all_signatures.extend(build_signatures(records))

    touched = [
        signature
        for signature in all_signatures
        if signature.file_path in changed
        and signature_touched(signature, changed[signature.file_path], sources.get(signature.file_path, ""))
    ]

    results = [
        validate_contract_against_source(signature, sources[signature.file_path])
        for signature in touched
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

    return ProjectReport(project_path=str(root), status=status, results=results)


def validate_selected_paths(
    root: str | Path,
    files: list[str],
    *,
    manifest: str | Path | None = None,
    full_graph: bool = False,
):
    if full_graph:
        from .project import validate_project

        manifest_path = manifest
        if manifest_path is None:
            root_path = Path(root)
            for candidate in MANIFEST_NAMES:
                path = root_path / candidate
                if path.exists():
                    manifest_path = path
                    break
        return validate_project(root, manifest_path=manifest_path)

    sources = load_selected_sources(root, files)

    manifest_records = None
    if manifest:
        manifest_path = Path(manifest)
        if not manifest_path.is_absolute():
            manifest_path = Path(root) / manifest_path
        if manifest_path.exists():
            manifest_records = load_manifest_records(manifest_path)

    return validate_sources(sources, manifest_records=manifest_records)


def staged_check(
    root: str | Path = ".",
    *,
    manifest: str | Path | None = None,
    hunk_filter: bool = False,
):
    changes = staged_files(root)
    files = paths_from_changes(changes)
    diff_text = staged_hunks(root)
    hunks = parse_unified_diff_hunks(diff_text)
    full_graph = _manifest_changed(files)

    if full_graph:
        report = validate_selected_paths(root, files, manifest=manifest, full_graph=True)
    elif hunk_filter and hunks:
        report = validate_sources_for_hunks(root, files, hunks, manifest=manifest)
    else:
        report = validate_selected_paths(root, files, manifest=manifest)

    return report, files, hunks


def changed_check(root: str | Path = ".", *, base_ref: str = "main", manifest: str | Path | None = None):
    changes = changed_files(root, base_ref=base_ref)
    files = paths_from_changes(changes)
    full_graph = _manifest_changed(files)
    report = validate_selected_paths(root, files, manifest=manifest, full_graph=full_graph)
    return report, files, []
