from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from intract.plugins.base import infer_language


SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", "dist", "build", ".intract"}
DEFAULT_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".cs", ".java", ".go", ".rs", ".php", ".rb", ".sh"}


@dataclass(frozen=True)
class SourceUnit:
    path: str
    language: str | None
    text: str


def collect_source_units(
    root: str | Path,
    *,
    extensions: set[str] | None = None,
    max_file_size: int = 512_000,
) -> list[SourceUnit]:
    root = Path(root)
    extensions = extensions or DEFAULT_EXTENSIONS
    units: list[SourceUnit] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.suffix.lower() not in extensions:
            continue
        if path.stat().st_size > max_file_size:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        units.append(
            SourceUnit(
                path=str(path.relative_to(root)),
                language=infer_language(str(path)),
                text=text,
            )
        )

    return units
