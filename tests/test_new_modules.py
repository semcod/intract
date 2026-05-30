from pathlib import Path

from intract.coverage import calculate_coverage
from intract.duplicates import find_duplicate_contracts
from intract.graph import build_graph


def test_coverage(tmp_path: Path):
    (tmp_path / "a.py").write_text(
        "# @intract.v1 scope:function intent:parse:extensions priority:2\n"
        "def parse_extensions(raw):\n"
        "    return raw.split(',')\n",
        encoding="utf-8",
    )
    report = calculate_coverage(tmp_path)
    assert report.files_total == 1
    assert report.contracts_total == 1


def test_duplicates(tmp_path: Path):
    (tmp_path / "a.py").write_text(
        "# @intract.v1 scope:function intent:parse:extensions priority:2 domain:cli\n"
        "def parse_extensions(raw):\n"
        "    return raw.split(',')\n",
        encoding="utf-8",
    )
    (tmp_path / "b.py").write_text(
        "# @intract.v1 scope:function intent:parse:extension_list priority:2 domain:cli\n"
        "def load_extensions(raw):\n"
        "    return raw.split(',')\n",
        encoding="utf-8",
    )
    matches = find_duplicate_contracts(tmp_path, threshold=0.5)
    assert matches


def test_graph_missing_requirement(tmp_path: Path):
    (tmp_path / "intract.yaml").write_text(
        "contracts:\n"
        "  - id: p\n"
        "    scope: project\n"
        "    intent: analyze:code\n"
        "    require:\n"
        "      - scan.project_files\n",
        encoding="utf-8",
    )
    graph = build_graph(tmp_path)
    assert "scan.project_file" in graph.missing
