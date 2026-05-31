from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class ValidationStatus(str, Enum):
    PASS = "pass"
    PARTIAL = "partial"
    FAIL = "fail"
    VIOLATION = "violation"
    UNKNOWN = "unknown"


VALID_SCOPES = {
    "line",
    "block",
    "function",
    "method",
    "class",
    "file",
    "module",
    "package",
    "project",
    "ui",
}


@dataclass(frozen=True)
class Contract:
    action: str
    object: str
    scope: str = "block"
    priority: int = 3
    domain: str = ""
    inputs: tuple[str, ...] = field(default_factory=tuple)
    outputs: tuple[str, ...] = field(default_factory=tuple)
    effects: tuple[str, ...] = field(default_factory=tuple)
    forbidden: tuple[str, ...] = field(default_factory=tuple)
    required: tuple[str, ...] = field(default_factory=tuple)
    validators: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    algorithms: tuple[str, ...] = field(default_factory=tuple)
    relations: tuple[str, ...] = field(default_factory=tuple)
    contract_id: str = ""
    meaning: str = ""
    raw: str = ""

    @property
    def key(self) -> str:
        return f"{self.action}.{self.object}"


@dataclass(frozen=True)
class ContractRecord:
    contract: Contract
    file_path: str
    start_line: int
    end_line: int
    owner: str = ""


@dataclass(frozen=True)
class ContractSignature:
    block_id: str
    file_path: str
    start_line: int
    end_line: int
    scope: str
    action: str
    object: str
    domain: str
    priority: int
    inputs: frozenset[str] = field(default_factory=frozenset)
    outputs: frozenset[str] = field(default_factory=frozenset)
    effects: frozenset[str] = field(default_factory=frozenset)
    forbidden: frozenset[str] = field(default_factory=frozenset)
    required: frozenset[str] = field(default_factory=frozenset)
    validators: frozenset[str] = field(default_factory=frozenset)
    tags: frozenset[str] = field(default_factory=frozenset)
    algorithms: frozenset[str] = field(default_factory=frozenset)
    relations: frozenset[str] = field(default_factory=frozenset)
    features: frozenset[str] = field(default_factory=frozenset)
    exact_hash: str = ""
    raw: str = ""
    meaning: str = ""

    @property
    def key(self) -> str:
        return f"{self.action}.{self.object}"


@dataclass(frozen=True)
class ValidationIssue:
    kind: str
    message: str
    severity: str = "error"


@dataclass
class ValidationResult:
    contract: str
    scope: str
    status: ValidationStatus
    score: float = 0.0
    file_path: str | None = None
    lines: tuple[int, int] | None = None
    matched: dict[str, Any] = field(default_factory=dict)
    missing: list[str] = field(default_factory=list)
    violations: list[ValidationIssue] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data


@dataclass
class ProjectReport:
    project_path: str
    status: ValidationStatus
    results: list[ValidationResult] = field(default_factory=list)

    @property
    def passed(self) -> list[ValidationResult]:
        return [item for item in self.results if item.status == ValidationStatus.PASS]

    @property
    def partial(self) -> list[ValidationResult]:
        return [item for item in self.results if item.status == ValidationStatus.PARTIAL]

    @property
    def failed(self) -> list[ValidationResult]:
        return [item for item in self.results if item.status == ValidationStatus.FAIL]

    @property
    def violations(self) -> list[ValidationResult]:
        return [item for item in self.results if item.status == ValidationStatus.VIOLATION]

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_path": self.project_path,
            "status": self.status.value,
            "summary": {
                "total": len(self.results),
                "passed": len(self.passed),
                "partial": len(self.partial),
                "failed": len(self.failed),
                "violations": len(self.violations),
            },
            "results": [item.to_dict() for item in self.results],
        }
