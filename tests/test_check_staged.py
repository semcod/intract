from pathlib import Path

from intract.check import _manifest_changed, validate_selected_paths


def test_manifest_changed_helper():
    assert _manifest_changed(["intract.yaml"])
    assert not _manifest_changed(["src/app.py"])


def test_validate_selected_paths_full_graph(tmp_path: Path):
    (tmp_path / "intract.yaml").write_text(
        "contracts:\n"
        "  - scope: project\n"
        "    intent: analyze:code\n"
        "    require:\n"
        "      - scan.project_files\n",
        encoding="utf-8",
    )
    (tmp_path / "worker.py").write_text(
        "# @intract.v1 scope:function intent:scan:project_files\n"
        "def scan():\n"
        "    return []\n",
        encoding="utf-8",
    )

    report = validate_selected_paths(
        tmp_path,
        ["intract.yaml"],
        manifest=tmp_path / "intract.yaml",
        full_graph=True,
    )
    assert report.results
    assert report.project_path == str(tmp_path)
