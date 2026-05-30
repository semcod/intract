from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path

from .project import load_project_sources, extract_signatures_from_sources


@dataclass(frozen=True)
class CoverageReport:
    files_total: int
    files_with_contracts: int
    contracts_total: int
    coverage_percent: float
    missing_files: list[str]

    def to_dict(self):
        return asdict(self)


def calculate_coverage(root: str | Path = ".") -> CoverageReport:
    root = Path(root)
    sources = load_project_sources(root)
    signatures = extract_signatures_from_sources(sources)
    files_with = sorted({s.file_path for s in signatures})
    missing = sorted(set(sources) - set(files_with))
    coverage = (len(files_with) / len(sources) * 100.0) if sources else 0.0
    return CoverageReport(
        files_total=len(sources),
        files_with_contracts=len(files_with),
        contracts_total=len(signatures),
        coverage_percent=round(coverage, 2),
        missing_files=missing,
    )
