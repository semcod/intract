from __future__ import annotations

import re

from .blocks import block_extent_from_patterns

RUST_START = [
    re.compile(r"^\s*(?:pub\s+)?(?:async\s+)?fn\s+\w+\s*\("),
    re.compile(r"^\s*(?:pub\s+)?impl(?:<[^>]+>)?\s+\w+"),
    re.compile(r"^\s*(?:pub\s+)?struct\s+\w+"),
]


def rust_block_extent(source: str, start_line: int) -> tuple[int, int]:
    return block_extent_from_patterns(source, start_line, RUST_START)
