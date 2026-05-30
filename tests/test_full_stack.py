from pathlib import Path

from intract.duplicates import find_duplicate_contracts
from intract.graph import build_graph
from intract.project import validate_project


ROOT = Path(__file__).resolve().parents[1] / "examples" / "full-stack"


def test_full_stack_validate_passes():
    report = validate_project(ROOT, manifest_path=ROOT / "intract.yaml")
    assert report.status.value in {"pass", "partial"}


def test_full_stack_graph_covers_requires():
    graph = build_graph(ROOT, manifest=ROOT / "intract.yaml")
    assert "scan.project_file" not in graph.missing
    assert "parse.extension" not in graph.missing
    assert "detect.duplicate" not in graph.missing


def test_full_stack_finds_intent_duplicates():
    matches = find_duplicate_contracts(ROOT, threshold=0.5)
    contracts = {item.left_contract for item in matches} | {item.right_contract for item in matches}
    assert "parse.extension" in contracts or "parse.extensions" in contracts
    assert len(matches) >= 1
