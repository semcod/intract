from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GitChange:
    path: str
    status: str = "modified"


def _run_git(args: list[str], root: str | Path = ".") -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=str(root), text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return ""


def staged_files(root: str | Path = ".") -> list[GitChange]:
    out = _run_git(["diff", "--cached", "--name-status", "--diff-filter=ACMR"], root)
    changes: list[GitChange] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            changes.append(GitChange(path=parts[1], status=parts[0]))
    return changes


def changed_files(root: str | Path = ".", base_ref: str = "main") -> list[GitChange]:
    out = _run_git(["diff", "--name-status", "--diff-filter=ACMR", f"{base_ref}...HEAD"], root)
    changes: list[GitChange] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            changes.append(GitChange(path=parts[1], status=parts[0]))
    return changes


def staged_hunks(root: str | Path = ".", path: str | None = None) -> str:
    args = ["diff", "--cached", "--unified=0"]
    if path:
        args.extend(["--", path])
    return _run_git(args, root)


def paths_from_changes(changes: list[GitChange]) -> list[str]:
    return sorted({c.path for c in changes})
