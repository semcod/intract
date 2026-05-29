from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class EngineConfig:
    root: Path
    manifest: str | None = "intract.yaml"
    state_path: str = ".intract/engine-state.json"
    include_tests: bool = False
    max_file_size: int = 512_000


@dataclass(frozen=True)
class LogicalFragment:
    id: str
    file_path: str
    kind: str
    name: str
    start_line: int
    end_line: int
    text: str
    language: str | None = None


@dataclass(frozen=True)
class ContractSuggestion:
    fragment_id: str
    file_path: str
    line: int
    contract_line: str
    confidence: float
    reason: str
    metadata: dict[str, object] = field(default_factory=dict)
