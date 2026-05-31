from pathlib import Path

from intract.project import validate_project


ROOT = Path(__file__).resolve().parents[1] / "examples" / "web-app"
MANIFEST = ROOT / "intract.yaml"


def test_web_app_v1_overall_pass():
    report = validate_project(ROOT / "iterations/v1-pass", manifest_path=MANIFEST)
    function_results = [r for r in report.results if r.scope == "function"]
    assert function_results
    assert all(r.status.value == "pass" for r in function_results)
    assert report.status.value == "pass"


def test_web_app_v2_has_network_violations():
    report = validate_project(ROOT / "iterations/v2-violation", manifest_path=MANIFEST)
    violated = {r.contract for r in report.violations}
    assert "auth.check_permission" in violated
    assert "ui.render_dashboard" in violated


def test_web_app_graph_has_no_missing_requires():
    from intract.graph import build_graph

    graph = build_graph(ROOT / "iterations/v1-pass", manifest=MANIFEST)
    assert "auth.check_permission" not in graph.missing
    assert "api.read_profile" not in graph.missing
    assert "deploy.container_image" not in graph.missing
