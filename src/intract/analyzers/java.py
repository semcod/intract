from __future__ import annotations

import re

from .blocks import block_extent_from_patterns

JAVA_START = [
    re.compile(
        r"^\s*(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?"
        r"[\w<>\[\],?\s]+\s+\w+\s*\(",
    ),
    re.compile(r"^\s*(?:public|private|protected)?\s*(?:abstract\s+)?class\s+\w+"),
    re.compile(r"^\s*@\w+"),
]


def java_block_extent(source: str, start_line: int) -> tuple[int, int]:
    extent = block_extent_from_patterns(source, start_line, JAVA_START)
    if extent[0] != extent[1]:
        return extent

    lines = source.splitlines()
    for index in range(start_line, len(lines) + 1):
        if lines[index - 1].strip().startswith("@"):
            continue
        return block_extent_from_patterns(source, index, JAVA_START[:2])
    return start_line, start_line
