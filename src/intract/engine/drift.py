from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .context import LogicalFragment


@dataclass(frozen=True)
class FragmentState:
    id: str
    file_path: str
    kind: str
    name: str
    start_line: int
    end_line: int
    text_hash: str


@dataclass(frozen=True)
class DriftIssue:
    kind: str
    fragment_id: str
    file_path: str
    message: str
    severity: str = "warning"


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def state_from_fragments(fragments: list[LogicalFragment]) -> dict[str, FragmentState]:
    return {
        fragment.id: FragmentState(
            id=fragment.id,
            file_path=fragment.file_path,
            kind=fragment.kind,
            name=fragment.name,
            start_line=fragment.start_line,
            end_line=fragment.end_line,
            text_hash=hash_text(fragment.text),
        )
        for fragment in fragments
    }


def save_state(path: str | Path, fragments: list[LogicalFragment]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    data = {k: asdict(v) for k, v in state_from_fragments(fragments).items()}
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_state(path: str | Path) -> dict[str, FragmentState]:
    p = Path(path)
    if not p.exists():
        return {}

    raw = json.loads(p.read_text(encoding="utf-8"))
    return {k: FragmentState(**v) for k, v in raw.items()}


def detect_drift(
    previous: dict[str, FragmentState],
    current_fragments: list[LogicalFragment],
) -> list[DriftIssue]:
    current = state_from_fragments(current_fragments)
    issues: list[DriftIssue] = []

    previous_ids = set(previous)
    current_ids = set(current)

    for fragment_id in sorted(previous_ids - current_ids):
        old = previous[fragment_id]
        issues.append(
            DriftIssue(
                kind="removed_fragment",
                fragment_id=fragment_id,
                file_path=old.file_path,
                message=f"Previously known {old.kind} '{old.name}' disappeared.",
            )
        )

    for fragment_id in sorted(current_ids - previous_ids):
        new = current[fragment_id]
        issues.append(
            DriftIssue(
                kind="new_fragment",
                fragment_id=fragment_id,
                file_path=new.file_path,
                message=f"New {new.kind} '{new.name}' appeared and may need an Intract contract.",
                severity="info",
            )
        )

    for fragment_id in sorted(previous_ids & current_ids):
        old = previous[fragment_id]
        new = current[fragment_id]
        if old.text_hash != new.text_hash:
            issues.append(
                DriftIssue(
                    kind="logic_changed",
                    fragment_id=fragment_id,
                    file_path=new.file_path,
                    message=f"Logic changed in {new.kind} '{new.name}'. Re-validate expected Intract contract.",
                    severity="warning",
                )
            )

    return issues
