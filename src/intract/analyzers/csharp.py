from __future__ import annotations

import re


CS_METHOD = re.compile(
    r"^\s*(?:\[(?:[^\]]+)\]\s*)?"
    r"(?:public|private|protected|internal)\s+"
    r"(?:static\s+)?(?:async\s+)?"
    r"[\w<>\[\]?,\s]+\s+\w+\s*\(",
    re.MULTILINE,
)
CS_CLASS = re.compile(r"^\s*(?:public|private|protected|internal)?\s*(?:partial\s+)?class\s+\w+", re.MULTILINE)


def csharp_block_extent(source: str, start_line: int) -> tuple[int, int]:
    lines = source.splitlines()
    if start_line < 1 or start_line > len(lines):
        return start_line, start_line

    treesitter_extent = _treesitter_csharp_extent(source, start_line)
    if treesitter_extent is not None:
        return start_line, treesitter_extent[1]

    block_start = None
    for index in range(start_line, len(lines) + 1):
        line = lines[index - 1]
        if CS_METHOD.match(line) or CS_CLASS.match(line):
            block_start = index
            break

    if block_start is None:
        return start_line, start_line

    end = _scan_braced_block(lines, block_start)
    return start_line, end


def _scan_braced_block(lines: list[str], start_line: int) -> int:
    depth = 0
    started = False
    end = start_line

    for index in range(start_line, len(lines) + 1):
        line = lines[index - 1]
        for char in line:
            if char == "{":
                depth += 1
                started = True
            elif char == "}":
                depth -= 1
                if started and depth == 0:
                    return index
        if started:
            end = index

    return end


def _treesitter_csharp_extent(source: str, start_line: int) -> tuple[int, int] | None:
    try:
        from intract.analyzers.treesitter import csharp_method_extent
    except ImportError:
        return None
    return csharp_method_extent(source, start_line)
