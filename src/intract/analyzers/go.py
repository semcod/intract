from __future__ import annotations

import re

from .blocks import block_extent_from_patterns

GO_START = [
    re.compile(r"^\s*func\s+(?:\([^)]*\)\s+)?\w+\s*\("),
]


def go_block_extent(source: str, start_line: int) -> tuple[int, int]:
    return block_extent_from_patterns(source, start_line, GO_START)
