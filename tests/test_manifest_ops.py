import json
from pathlib import Path

from intract.manifest_ops import apply_ledger_to_manifest, contract_line_to_manifest_entry


def test_contract_line_to_manifest_entry_parses_ui_line():
    line = (
        '@intract.v1 id:cinema.test.S0.ui.remove.Mod scope:ui intent:ui:remove:Mod '
        'priority:3 domain:calculator effect:ui_change forbid:destructive_write '
        'require:human_review validate:no_forbidden_effect '
        'meaning:"Cinema S0 removed #Mod"'
    )
    entry = contract_line_to_manifest_entry(line)
    assert entry is not None
    assert entry["id"] == "cinema.test.S0.ui.remove.Mod"
    assert entry["scope"] == "ui"
    assert "remove" in entry["intent"]


def test_apply_ledger_to_manifest_adds_only_evolved(tmp_path: Path):
    manifest = tmp_path / "intract.yaml"
    manifest.write_text(
        "version: intract.v1\ncontracts:\n  - id: existing\n    scope: project\n    intent: keep:me\n",
        encoding="utf-8",
    )
    ledger = tmp_path / "ledger.json"
    ledger.write_text(
        json.dumps(
            [
                {
                    "status": "evolved_by_llm",
                    "proposed_contracts": [
                        {
                            "line": (
                                '@intract.v1 id:cinema.caps.S0.ui.remove.X scope:ui '
                                'intent:ui:remove:X priority:3 domain:ui effect:ui_change '
                                'forbid:destructive_write validate:no_forbidden_effect '
                                'meaning:"removed X"'
                            )
                        }
                    ],
                },
                {
                    "status": "llm_skipped: noop",
                    "proposed_contracts": [
                        {
                            "line": (
                                '@intract.v1 id:cinema.caps.S0.ui.remove.Y scope:ui '
                                'intent:ui:remove:Y priority:3 domain:ui effect:ui_change '
                                'forbid:destructive_write validate:no_forbidden_effect '
                                'meaning:"skipped"'
                            )
                        }
                    ],
                },
            ]
        ),
        encoding="utf-8",
    )

    result = apply_ledger_to_manifest(manifest, ledger)
    assert result.added == ["cinema.caps.S0.ui.remove.X"]
    text = manifest.read_text(encoding="utf-8")
    assert "cinema.caps.S0.ui.remove.X" in text
    assert "cinema.caps.S0.ui.remove.Y" not in text


def test_apply_ledger_to_manifests_both_targets(tmp_path: Path):
    from intract.manifest_ops import apply_ledger_to_manifests

    workspace = tmp_path / "ws"
    workspace.mkdir()
    project_manifest = workspace / "intract.yaml"
    project_manifest.write_text("version: intract.v1\ncontracts: []\n", encoding="utf-8")
    capsule_dir = workspace / ".nexu" / "capsules" / "demo"
    capsule_dir.mkdir(parents=True)
    capsule_manifest = capsule_dir / "intract.yaml"
    capsule_manifest.write_text("version: intract.v1\ncontracts: []\n", encoding="utf-8")
    ledger = tmp_path / "ledger.json"
    line = (
        '@intract.v1 id:cinema.demo.S0.ui.remove.Z scope:ui intent:ui:remove:Z '
        'priority:3 domain:ui effect:ui_change forbid:destructive_write '
        'validate:no_forbidden_effect meaning:"removed Z"'
    )
    ledger.write_text(
        json.dumps(
            [
                {
                    "status": "evolved_by_llm",
                    "proposed_contracts": [{"line": line}],
                }
            ]
        ),
        encoding="utf-8",
    )

    batch = apply_ledger_to_manifests(
        workspace_root=workspace,
        capsule_name="demo",
        ledger_path=ledger,
        target="both",
    )
    assert batch.added_total == 2
    assert "cinema.demo.S0.ui.remove.Z" in project_manifest.read_text(encoding="utf-8")
    assert "cinema.demo.S0.ui.remove.Z" in capsule_manifest.read_text(encoding="utf-8")
