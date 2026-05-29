from __future__ import annotations

import hashlib
import re

from .context import LogicalFragment
from .scanner import SourceUnit


PY_FUNC = re.compile(r"^(?P<indent>\s*)def\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\(", re.MULTILINE)
PY_CLASS = re.compile(r"^(?P<indent>\s*)class\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*[:(]", re.MULTILINE)
JS_FUNC = re.compile(
    r"(function\s+(?P<name1>[A-Za-z_][A-Za-z0-9_]*)\s*\(|"
    r"(?:const|let|var)\s+(?P<name2>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*"
    r"(?:async\s*)?\(?[^=]*\)?\s*=>)",
    re.MULTILINE,
)
CS_FUNC = re.compile(
    r"\b(?:public|private|protected|internal)?\s*(?:static\s+)?"
    r"[A-Za-z0-9_<>,\[\]]+\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\(",
    re.MULTILINE,
)


def _line_number(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _fragment_id(path: str, kind: str, name: str, start: int, end: int) -> str:
    raw = f"{path}:{kind}:{name}:{start}:{end}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def _slice_until_next_match(text: str, start_pos: int, next_positions: list[int]) -> tuple[int, str]:
    next_pos = min([p for p in next_positions if p > start_pos], default=len(text))
    return next_pos, text[start_pos:next_pos]


def analyze_source_units(units: list[SourceUnit]) -> list[LogicalFragment]:
    fragments: list[LogicalFragment] = []

    for unit in units:
        patterns = []
        if unit.language == "python":
            patterns = [(PY_CLASS, "class"), (PY_FUNC, "function")]
        elif unit.language in {"javascript", "typescript"}:
            patterns = [(JS_FUNC, "function")]
        elif unit.language == "csharp":
            patterns = [(CS_FUNC, "method")]
        else:
            patterns = [(PY_FUNC, "function"), (JS_FUNC, "function"), (CS_FUNC, "method")]

        matches = []
        for pattern, kind in patterns:
            for match in pattern.finditer(unit.text):
                name = (
                    match.groupdict().get("name")
                    or match.groupdict().get("name1")
                    or match.groupdict().get("name2")
                    or "unknown"
                )
                matches.append((match.start(), match.end(), kind, name))

        matches.sort(key=lambda x: x[0])
        positions = [m[0] for m in matches]

        for start_pos, _, kind, name in matches:
            end_pos, body = _slice_until_next_match(unit.text, start_pos, positions)
            start_line = _line_number(unit.text, start_pos)
            end_line = _line_number(unit.text, end_pos)

            fragments.append(
                LogicalFragment(
                    id=_fragment_id(unit.path, kind, name, start_line, end_line),
                    file_path=unit.path,
                    kind=kind,
                    name=name,
                    start_line=start_line,
                    end_line=end_line,
                    text=body,
                    language=unit.language,
                )
            )

    return fragments
