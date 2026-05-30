from pathlib import Path

from intract.graph import build_graph
from intract.policy import decide_policy
from intract.project import validate_project


def test_missing_required_p1_fails_policy(tmp_path: Path):
    (tmp_path / "intract.yaml").write_text(
        "contracts:\n"
        "  - id: p\n"
        "    scope: project\n"
        "    intent: analyze:code\n"
        "    priority: 1\n"
        "    require:\n"
        "      - scan.project_files\n",
        encoding="utf-8",
    )

    report = validate_project(tmp_path, manifest_path=tmp_path / "intract.yaml")
    graph = build_graph(tmp_path, manifest=tmp_path / "intract.yaml")
    decision = decide_policy(
        report,
        fail_on=["missing_required_p1"],
        graph=graph,
        manifest_path=tmp_path / "intract.yaml",
    )

    assert decision.should_fail
    assert any("missing_required_p1" in reason for reason in decision.reasons)


def test_full_stack_passes_without_p1_gate():
    root = Path(__file__).resolve().parents[1] / "examples" / "full-stack"
    manifest = root / "intract.yaml"
    report = validate_project(root, manifest_path=manifest)
    graph = build_graph(root, manifest=manifest)
    decision = decide_policy(
        report,
        fail_on=["violation", "missing_required_p1"],
        graph=graph,
        manifest_path=manifest,
    )

    assert not decision.should_fail
