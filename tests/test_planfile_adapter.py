from pathlib import Path

from intract.integrations.planfile import tickets_from_report
from intract.integrations.planfile_adapter import PlanfileApiAdapter, PlanfileConfig
from intract.project import validate_project


def test_planfile_push_local_only(tmp_path: Path):
    (tmp_path / "bad.py").write_text(
        "# @intract.v1 scope:function intent:validate:user forbid:network\n"
        "import requests\n"
        "def validate_user():\n"
        "    return requests.get('https://example.com')\n",
        encoding="utf-8",
    )
    report = validate_project(tmp_path)
    adapter = PlanfileApiAdapter(PlanfileConfig(output_dir=tmp_path / ".intract"))
    result = adapter.push(tickets_from_report(report))

    assert result.pushed >= 1
    assert result.remote_status == "local-only"
    assert (tmp_path / ".intract" / "planfile-tickets.json").exists()


def test_planfile_pull_reads_local_export(tmp_path: Path):
    (tmp_path / "bad.py").write_text(
        "# @intract.v1 scope:function intent:validate:user forbid:network\n"
        "import requests\n"
        "def validate_user():\n"
        "    return requests.get('https://example.com')\n",
        encoding="utf-8",
    )
    report = validate_project(tmp_path)
    adapter = PlanfileApiAdapter(PlanfileConfig(output_dir=tmp_path / ".intract"))
    adapter.push(tickets_from_report(report))
    pulled = adapter.pull()

    assert pulled
    assert pulled[0].source == "intract"
