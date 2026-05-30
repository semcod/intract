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


def validate_selected_paths(
    root: str | Path,
    files: list[str],
    *,
    manifest: str | Path | None = None,
):
    sources = load_selected_sources(root, files)

    manifest_records = None
    if manifest:
        manifest_path = Path(manifest)
        if not manifest_path.is_absolute():
            manifest_path = Path(root) / manifest_path
        if manifest_path.exists():
            manifest_records = load_manifest_records(manifest_path)

    return validate_sources(sources, manifest_records=manifest_records)


def staged_check(root: str | Path = ".", *, manifest: str | Path | None = None):
    changes = staged_files(root)
    files = paths_from_changes(changes)
    diff_text = staged_hunks(root)
    hunks = parse_unified_diff_hunks(diff_text)
    return validate_selected_paths(root, files, manifest=manifest), files, hunks


def changed_check(root: str | Path = ".", *, base_ref: str = "main", manifest: str | Path | None = None):
    changes = changed_files(root, base_ref=base_ref)
    files = paths_from_changes(changes)
    return validate_selected_paths(root, files, manifest=manifest), files, []
