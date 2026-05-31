from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

# Make package importable when running from source tree.
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from intract.engine import EngineConfig, scan_suggest_and_validate
from intract.integrations.planfile import PlanfileExporter, tickets_from_report
from intract.project import validate_project
from intract.watch import WatchConfig, diff_snapshots, snapshot_tree


def print_result(name: str, payload: dict) -> None:
    print(f"\n=== {name} ===")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def run_example_01(base: Path) -> dict:
    path = base / "01_python_pass"
    report = validate_project(path)
    return {
        "status": report.status.value,
        "total": len(report.results),
        "passed": len(report.passed),
        "violations": len(report.violations),
    }


def run_example_02(base: Path) -> dict:
    path = base / "02_typescript_violation_planfile"
    report = validate_project(path)
    tickets = tickets_from_report(report)
    exported = PlanfileExporter(path / ".intract").export(tickets)
    return {
        "status": report.status.value,
        "total": len(report.results),
        "violations": len(report.violations),
        "tickets": len(tickets),
        "ticket_files": {k: str(v.relative_to(path)) for k, v in exported.items()},
    }


def run_example_03(base: Path) -> dict:
    path = base / "03_watch_engine_drift"
    state_dir = path / ".intract"
    if state_dir.exists():
        shutil.rmtree(state_dir)

    before = snapshot_tree(path, WatchConfig(interval=0.1))
    scanner = path / "scanner.py"
    original = scanner.read_text(encoding="utf-8")
    scanner.write_text(original.replace('path.endswith(".py")', 'path.strip().endswith(".py")'), encoding="utf-8")
    after = snapshot_tree(path, WatchConfig(interval=0.1))
    changes = diff_snapshots(before, after)

    engine = scan_suggest_and_validate(
        EngineConfig(root=path, manifest=None, state_path=str(path / ".intract" / "state.json"))
    )

    # Restore file to avoid leaving example modified.
    scanner.write_text(original, encoding="utf-8")

    return {
        "watch_changes": len(changes),
        "engine_fragments": engine["fragments"],
        "engine_suggestions": len(engine["suggestions"]),
        "drift_issues": len(engine["drift"]),
        "validation_status": engine["validation"]["status"],
    }


def run_example_04(base: Path) -> dict:
    web = base.parent / "web-app"
    manifest = web / "intract.yaml"
    v1 = validate_project(web / "iterations/v1-pass", manifest_path=manifest)
    v2 = validate_project(web / "iterations/v2-violation", manifest_path=manifest)
    return {
        "v1_status": v1.status.value,
        "v2_status": v2.status.value,
        "v2_violations": len(v2.violations),
    }


def main() -> int:
    base = Path(__file__).resolve().parent
    results = {
        "example_01": run_example_01(base),
        "example_02": run_example_02(base),
        "example_03": run_example_03(base),
        "example_04": run_example_04(base),
    }

    for name, payload in results.items():
        print_result(name, payload)

    assert results["example_01"]["status"] == "pass"
    assert results["example_02"]["status"] == "violation"
    assert results["example_02"]["tickets"] >= 1
    assert results["example_03"]["watch_changes"] >= 1
    assert results["example_03"]["engine_fragments"] >= 1
    assert results["example_04"]["v1_status"] == "pass"
    assert results["example_04"]["v2_status"] == "violation"
    assert results["example_04"]["v2_violations"] >= 2

    print("\nAll integration examples passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
