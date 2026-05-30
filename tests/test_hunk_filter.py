from pathlib import Path

from intract.check import (
    ChangedHunk,
    block_extent,
    changed_lines_by_file,
    signature_touched,
    validate_sources_for_hunks,
)
from intract.core.models import ValidationStatus
from intract.core.signatures import build_signatures
from intract.parsers.inline import extract_contract_records_from_text


def test_changed_lines_by_file():
    hunks = [
        ChangedHunk("a.py", 1, 1, 10, 2, "func"),
        ChangedHunk("a.py", 5, 1, 20, 1, "func"),
    ]
    lines = changed_lines_by_file(hunks)
    assert lines["a.py"] == {10, 11, 20}


def test_block_extent_finds_function_body():
    source = (
        "# @intract.v1 scope:function intent:parse:extensions\n"
        "def parse_extensions(raw):\n"
        "    return raw.split(',')\n"
        "\n"
        "def other():\n"
        "    pass\n"
    )
    start, end = block_extent(source, 1)
    assert start == 1
    assert end >= 3


def test_signature_touched_by_body_change():
    source = (
        "# @intract.v1 scope:function intent:parse:extensions\n"
        "def parse_extensions(raw):\n"
        "    return raw.split(',')\n"
    )
    records = extract_contract_records_from_text(source, file_path="a.py")
    signature = build_signatures(records)[0]
    assert signature_touched(signature, {3}, source)
    assert not signature_touched(signature, {99}, source)


def test_validate_sources_for_hunks_only_touched_contract(tmp_path: Path):
    file_a = tmp_path / "a.py"
    file_b = tmp_path / "b.py"
    file_a.write_text(
        "# @intract.v1 scope:function intent:parse:extensions forbid:network\n"
        "def parse_extensions(raw):\n"
        "    return raw.split(',')\n",
        encoding="utf-8",
    )
    file_b.write_text(
        "# @intract.v1 scope:function intent:detect:duplicates forbid:network\n"
        "import requests\n"
        "def detect_duplicates(blocks):\n"
        "    return requests.get('https://example.com')\n",
        encoding="utf-8",
    )

    hunks = [ChangedHunk("a.py", 1, 1, 3, 1, "parse_extensions")]
    report = validate_sources_for_hunks(tmp_path, ["a.py", "b.py"], hunks)

    assert len(report.results) == 1
    assert report.results[0].contract.startswith("parse.extension")
    assert report.results[0].status == ValidationStatus.PASS


def test_validate_sources_for_hunks_catches_violation_in_touched_block(tmp_path: Path):
    path = tmp_path / "auth.py"
    path.write_text(
        "# @intract.v1 scope:function intent:validate:user forbid:network\n"
        "import requests\n"
        "def validate_user():\n"
        "    return requests.get('https://example.com')\n",
        encoding="utf-8",
    )

    hunks = [ChangedHunk("auth.py", 1, 1, 4, 1, "validate_user")]
    report = validate_sources_for_hunks(tmp_path, ["auth.py"], hunks)

    assert report.results[0].status == ValidationStatus.VIOLATION
