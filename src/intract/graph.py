from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .normalizer import normalize_requirement
from .project import load_project_sources, extract_signatures_from_sources
from .yaml_manifest import load_manifest_records
from .signature import build_signatures


@dataclass(frozen=True)
class ContractGraph:
    nodes: list[str]
    edges: list[tuple[str, str]]
    missing: list[str]

    def to_dict(self):
        return asdict(self)

    def to_mermaid(self) -> str:
        lines = ["graph TD"]
        for node in self.nodes:
            safe = _safe(node)
            lines.append(f'  {safe}["{node}"]')
        for src, dst in self.edges:
            lines.append(f"  {_safe(src)} --> {_safe(dst)}")
        for missing in self.missing:
            lines.append(f'  {_safe(missing)}["{missing} (missing)"]:::missing')
        if self.missing:
            lines.append("  classDef missing fill:#ffd6d6,stroke:#cc0000,color:#000;")
        return "\\n".join(lines)


def _safe(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value)


def build_graph(root: str | Path = ".", manifest: str | Path | None = None) -> ContractGraph:
    root = Path(root)
    sources = load_project_sources(root)
    observed = extract_signatures_from_sources(sources)
    all_signatures = list(observed)

    if manifest:
        manifest_path = Path(manifest)
    else:
        manifest_path = root / "intract.yaml"
        if not manifest_path.exists():
            manifest_path = root / "intent.yaml"

    if manifest_path.exists():
        all_signatures.extend(build_signatures(load_manifest_records(manifest_path)))

    nodes = sorted({s.key for s in all_signatures})
    node_set = set(nodes)
    edges: list[tuple[str, str]] = []
    missing: set[str] = set()

    for sig in all_signatures:
        for req in sig.required:
            req_norm = normalize_requirement(req)
            if req_norm:
                edges.append((sig.key, req_norm))
                if req_norm not in node_set:
                    missing.add(req_norm)

    return ContractGraph(nodes=nodes, edges=edges, missing=sorted(missing))
