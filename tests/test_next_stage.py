from pathlib import Path

from intract.artifacts import validate_artifact
from intract.check import parse_unified_diff_hunks
from intract.manifest_schema import validate_manifest


def test_manifest_schema_valid(tmp_path: Path):
    path = tmp_path / "intract.yaml"
    path.write_text(
        "contracts:\n"
        "  - scope: project\n"
        "    intent: analyze:code\n",
        encoding="utf-8",
    )
    report = validate_manifest(path)
    assert report.valid


def test_parse_hunks():
    diff = (
        "+++ b/src/a.py\n"
        "@@ -1,2 +1,3 @@ def a\n"
        "+x\n"
    )
    hunks = parse_unified_diff_hunks(diff)
    assert len(hunks) == 1
    assert hunks[0].file_path == "src/a.py"


def test_dockerfile_artifact_violation(tmp_path: Path):
    path = tmp_path / "Dockerfile"
    path.write_text("FROM python:latest\n", encoding="utf-8")
    report = validate_artifact(path)
    assert report.results
    assert report.results[0].status.value == "violation"
