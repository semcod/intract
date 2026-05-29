from pathlib import Path

from intract.yaml_manifest import load_manifest_records


def test_load_manifest_records(tmp_path: Path):
    manifest = tmp_path / "intent.yaml"
    manifest.write_text(
        "contracts:\n"
        "  - id: project.analysis\n"
        "    scope: project\n"
        "    intent: analyze:code_duplication\n"
        "    priority: 1\n"
        "    require:\n"
        "      - scan.project_files\n"
        "files:\n"
        "  src/scanner.py:\n"
        "    - scope: file\n"
        "      intent: scan:project_files\n"
        "      priority: 1\n",
        encoding="utf-8",
    )
    records = load_manifest_records(manifest)
    assert len(records) == 2
    assert records[0].contract.action == "analyze"
    assert records[1].contract.action == "scan"
