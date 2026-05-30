from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )


def test_staged_hunk_check_fails_on_network_violation(tmp_path: Path):
    _git(tmp_path, "init")
    _git(tmp_path, "config", "user.email", "test@example.com")
    _git(tmp_path, "config", "user.name", "Intract Test")

    source = (
        "# @intract.v1 scope:function intent:validate:user forbid:network\n"
        "import requests\n"
        "def validate_user():\n"
        "    return requests.get('https://example.com')\n"
    )
    target = tmp_path / "auth.py"
    target.write_text(source, encoding="utf-8")
    _git(tmp_path, "add", "auth.py")

    result = subprocess.run(
        [sys.executable, "-m", "intract", "check", str(tmp_path), "--staged", "--hunks"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "violation" in result.stdout.lower() or "VIOLATION" in result.stdout


def test_staged_hunk_check_passes_clean_contract(tmp_path: Path):
    _git(tmp_path, "init")
    _git(tmp_path, "config", "user.email", "test@example.com")
    _git(tmp_path, "config", "user.name", "Intract Test")

    source = (
        "# @intract.v1 scope:function intent:parse:extensions forbid:network\n"
        "def parse_extensions(raw):\n"
        "    return raw.split(',')\n"
    )
    target = tmp_path / "parser.py"
    target.write_text(source, encoding="utf-8")
    _git(tmp_path, "add", "parser.py")

    result = subprocess.run(
        [sys.executable, "-m", "intract", "check", str(tmp_path), "--staged", "--hunks"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Violations: 0" in result.stdout or "violations=0" in result.stdout.lower()
