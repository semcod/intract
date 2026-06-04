from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

from intract.project import validate_project

ROOT = Path(__file__).resolve().parents[1] / "examples" / "markdown-generator"
MANIFEST = ROOT / "intract.yaml"


def _load_pass_generator():
    path = ROOT / "pass" / "generator.py"
    spec = importlib.util.spec_from_file_location("markdown_generator_pass", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_markdown_generator_pass_validates_and_generates_required_format():
    report = validate_project(ROOT / "pass", manifest_path=MANIFEST)
    assert report.status.value == "pass"

    generator = _load_pass_generator()
    topic = "Bezpieczne wdrażanie modeli LLM"
    markdown_document = generator.generate_markdown_document(topic)

    assert markdown_document.startswith(f"# {topic}\n")
    for section in generator.REQUIRED_SECTIONS:
        assert f"## {section}" in markdown_document
    assert "<" not in markdown_document
    assert ">" not in markdown_document


def test_markdown_generator_violation_flags_forbidden_effects():
    report = validate_project(ROOT / "violation", manifest_path=MANIFEST)
    assert report.status.value == "violation"

    messages = {
        issue.message
        for result in report.violations
        for issue in result.violations
    }
    assert any("forbid:network" in message for message in messages)
    assert any("forbid:write" in message for message in messages)


def test_markdown_guard_rejects_topic_drift_and_html_format():
    generator = _load_pass_generator()
    format_report = generator.guard_markdown_contract(
        "<h1>Promocja tygodnia</h1>\n<p>Treść spoza tematu.</p>",
        generator.REQUIRED_SECTIONS,
        "Bezpieczne wdrażanie modeli LLM",
    )

    assert not format_report["ok"]
    assert not format_report["has_h1"]
    assert not format_report["keeps_topic"]
    assert not format_report["has_required_sections"]
    assert not format_report["no_html"]


def test_markdown_generator_demo_script_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "demo.py")],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "pass status: pass" in result.stdout
    assert "violation status: violation" in result.stdout
    assert "Declared forbid:network" in result.stdout
    assert "Declared forbid:write" in result.stdout
