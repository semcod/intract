from pathlib import Path

from intract.scan_artifacts import discover_artifact_paths, scan_all_artifacts


def test_discover_dockerfile(tmp_path: Path):
    (tmp_path / "Dockerfile").write_text("FROM python:3.12-slim\nUSER app\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("print('x')\n", encoding="utf-8")

    paths = discover_artifact_paths(tmp_path)
    assert any(path.name == "Dockerfile" for path in paths)


def test_scan_all_artifacts_reports_violation(tmp_path: Path):
    (tmp_path / "Dockerfile").write_text("FROM python:latest\n", encoding="utf-8")
    report = scan_all_artifacts(tmp_path)
    assert report.artifacts == ["Dockerfile"]
    assert report.violations
