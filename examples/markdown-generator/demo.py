from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
SRC = REPO_ROOT / "src"


def _validate_project(path: Path, manifest_path: Path):
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    from intract.project import validate_project

    return validate_project(path, manifest_path=manifest_path)


def _load_pass_generator():
    path = ROOT / "pass" / "generator.py"
    spec = importlib.util.spec_from_file_location("markdown_generator_pass_demo", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load generator from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _violation_messages(report) -> list[str]:
    messages = []
    for result in report.violations:
        for issue in result.violations:
            if issue.message not in messages:
                messages.append(issue.message)
    return messages


def main() -> int:
    manifest = ROOT / "intract.yaml"
    topic = "Bezpieczne wdrazanie modeli LLM"

    generator = _load_pass_generator()
    markdown_document = generator.generate_markdown_document(topic)
    format_report = generator.guard_markdown_contract(
        markdown_document,
        generator.REQUIRED_SECTIONS,
        topic,
    )

    pass_report = _validate_project(ROOT / "pass", manifest)
    violation_report = _validate_project(ROOT / "violation", manifest)

    print("== Generated Markdown ==")
    print(markdown_document)
    print("== Runtime format guard ==")
    print(format_report)
    print("== Intract validation ==")
    print(f"pass status: {pass_report.status.value}")
    print(f"violation status: {violation_report.status.value}")
    for message in _violation_messages(violation_report):
        print(f"- {message}")

    return 0 if pass_report.status.value == "pass" and violation_report.violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
