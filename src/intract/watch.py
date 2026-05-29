from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable


DEFAULT_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cs", ".go", ".rs", ".php", ".rb",
    ".sh", ".sql", ".html", ".css", ".md", ".yaml", ".yml", ".json", ".toml",
    ".dockerfile", ""
}

DEFAULT_IGNORE_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules", "dist", "build",
    ".pytest_cache", ".ruff_cache", ".mypy_cache", ".intract"
}


@dataclass(frozen=True)
class FileState:
    path: str
    digest: str
    size: int
    mtime_ns: int


@dataclass(frozen=True)
class FileChange:
    path: str
    kind: str  # added | modified | deleted
    old_digest: str | None = None
    new_digest: str | None = None


@dataclass
class WatchConfig:
    interval: float = 1.0
    extensions: set[str] = field(default_factory=lambda: set(DEFAULT_EXTENSIONS))
    ignore_dirs: set[str] = field(default_factory=lambda: set(DEFAULT_IGNORE_DIRS))
    debounce_seconds: float = 0.25
    include_hidden: bool = False


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 256), b""):
            h.update(chunk)
    return h.hexdigest()


def should_scan(path: Path, root: Path, config: WatchConfig) -> bool:
    rel_parts = path.relative_to(root).parts

    if not config.include_hidden:
        if any(part.startswith(".") and part not in {".github"} for part in rel_parts):
            return False

    if any(part in config.ignore_dirs for part in rel_parts):
        return False

    if not path.is_file():
        return False

    name = path.name.lower()
    suffix = path.suffix.lower()

    if name == "dockerfile" or name.startswith("dockerfile."):
        return True

    return suffix in config.extensions


def snapshot_tree(root: Path | str, config: WatchConfig | None = None) -> dict[str, FileState]:
    root = Path(root)
    config = config or WatchConfig()
    snapshot: dict[str, FileState] = {}

    for path in root.rglob("*"):
        if not should_scan(path, root, config):
            continue

        rel = str(path.relative_to(root))
        stat = path.stat()
        snapshot[rel] = FileState(
            path=rel,
            digest=hash_file(path),
            size=stat.st_size,
            mtime_ns=stat.st_mtime_ns,
        )

    return snapshot


def diff_snapshots(
    old: dict[str, FileState],
    new: dict[str, FileState],
) -> list[FileChange]:
    changes: list[FileChange] = []

    old_keys = set(old)
    new_keys = set(new)

    for path in sorted(new_keys - old_keys):
        changes.append(FileChange(path=path, kind="added", new_digest=new[path].digest))

    for path in sorted(old_keys - new_keys):
        changes.append(FileChange(path=path, kind="deleted", old_digest=old[path].digest))

    for path in sorted(old_keys & new_keys):
        if old[path].digest != new[path].digest:
            changes.append(
                FileChange(
                    path=path,
                    kind="modified",
                    old_digest=old[path].digest,
                    new_digest=new[path].digest,
                )
            )

    return changes


def watch_tree(
    root: Path | str,
    callback: Callable[[list[FileChange]], None],
    *,
    config: WatchConfig | None = None,
    max_cycles: int | None = None,
) -> None:
    root = Path(root)
    config = config or WatchConfig()

    previous = snapshot_tree(root, config)
    cycles = 0

    while True:
        time.sleep(config.interval)
        current = snapshot_tree(root, config)
        changes = diff_snapshots(previous, current)

        if changes:
            time.sleep(config.debounce_seconds)
            current = snapshot_tree(root, config)
            changes = diff_snapshots(previous, current)

            if changes:
                callback(changes)
                previous = current

        cycles += 1
        if max_cycles is not None and cycles >= max_cycles:
            return


def changes_to_paths(changes: Iterable[FileChange]) -> list[str]:
    return sorted({change.path for change in changes if change.kind != "deleted"})
